#!/usr/bin/env python3
"""
Amazon Connect Configuration Review Tool
========================================

Este script se conecta a tu instancia de Amazon Connect y muestra
toda la configuración actual incluyendo instancias, colas, agentes,
flujos de contacto, números de teléfono y métricas básicas.

Requisitos:
- boto3 >= 1.26.0
- credenciales AWS configuradas (AWS CLI, variables de entorno, o IAM role)

Uso:
    python amazon_connect_review.py

Credenciales AWS:
- Por defecto usa el perfil default de AWS CLI
- Puedes especificar un perfil con AWS_PROFILE=mi-perfil python script.py
- O usar variables de entorno: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
"""

import boto3
import json
from datetime import datetime, timezone
from botocore.exceptions import ClientError, NoCredentialsError
import sys
from typing import Dict, List, Optional
import argparse


class AmazonConnectReviewer:
    """Clase principal para revisar configuración de Amazon Connect"""
    
    def __init__(self, region_name: str = 'us-east-1', profile_name: Optional[str] = None):
        """
        Inicializa el cliente de Amazon Connect
        
        Args:
            region_name: Región AWS (default: us-east-1)
            profile_name: Perfil AWS a usar (default: None para usar default)
        """
        try:
            if profile_name:
                session = boto3.Session(profile_name=profile_name)
                self.connect_client = session.client('connect', region_name=region_name)
            else:
                self.connect_client = boto3.client('connect', region_name=region_name)
            
            self.region = region_name
            print(f"✅ Conectado exitosamente a Amazon Connect en región: {region_name}")
            
        except NoCredentialsError:
            print("❌ Error: No se encontraron credenciales AWS.")
            print("Configura tus credenciales usando:")
            print("- aws configure")
            print("- Variables de entorno: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY")
            print("- IAM Role si ejecutas en EC2/Lambda")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error conectando a Amazon Connect: {str(e)}")
            sys.exit(1)

    def get_instances(self) -> List[Dict]:
        """Obtiene todas las instancias de Amazon Connect"""
        try:
            response = self.connect_client.list_instances()
            return response.get('InstanceSummaryList', [])
        except ClientError as e:
            print(f"❌ Error obteniendo instancias: {e}")
            return []

    def get_instance_details(self, instance_id: str) -> Optional[Dict]:
        """Obtiene detalles de una instancia específica"""
        try:
            response = self.connect_client.describe_instance(InstanceId=instance_id)
            return response.get('Instance', {})
        except ClientError as e:
            print(f"❌ Error obteniendo detalles de instancia {instance_id}: {e}")
            return None

    def get_queues(self, instance_id: str) -> List[Dict]:
        """Obtiene todas las colas de una instancia"""
        try:
            response = self.connect_client.list_queues(InstanceId=instance_id)
            return response.get('QueueSummaryList', [])
        except ClientError as e:
            print(f"❌ Error obteniendo colas: {e}")
            return []

    def get_users(self, instance_id: str) -> List[Dict]:
        """Obtiene todos los usuarios/agentes de una instancia"""
        try:
            response = self.connect_client.list_users(InstanceId=instance_id)
            return response.get('UserSummaryList', [])
        except ClientError as e:
            print(f"❌ Error obteniendo usuarios: {e}")
            return []

    def get_contact_flows(self, instance_id: str) -> List[Dict]:
        """Obtiene todos los flujos de contacto de una instancia"""
        try:
            response = self.connect_client.list_contact_flows(InstanceId=instance_id)
            return response.get('ContactFlowSummaryList', [])
        except ClientError as e:
            print(f"❌ Error obteniendo flujos de contacto: {e}")
            return []

    def get_phone_numbers(self, instance_id: str) -> List[Dict]:
        """Obtiene todos los números de teléfono de una instancia"""
        try:
            response = self.connect_client.list_phone_numbers(InstanceId=instance_id)
            return response.get('PhoneNumberSummaryList', [])
        except ClientError as e:
            print(f"❌ Error obteniendo números de teléfono: {e}")
            return []

    def get_hours_of_operations(self, instance_id: str) -> List[Dict]:
        """Obtiene horarios de operación de una instancia"""
        try:
            response = self.connect_client.list_hours_of_operations(InstanceId=instance_id)
            return response.get('HoursOfOperationSummaryList', [])
        except ClientError as e:
            print(f"❌ Error obteniendo horarios de operación: {e}")
            return []

    def print_separator(self, title: str):
        """Imprime un separador visual con título"""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print('='*60)

    def print_instances_summary(self, instances: List[Dict]):
        """Imprime resumen de instancias"""
        self.print_separator("📋 INSTANCIAS DE AMAZON CONNECT")
        
        if not instances:
            print("❌ No se encontraron instancias de Amazon Connect")
            return
            
        print(f"Total de instancias: {len(instances)}\n")
        
        for i, instance in enumerate(instances, 1):
            print(f"{i}. {instance.get('InstanceAlias', 'Sin alias')}")
            print(f"   ID: {instance.get('Id')}")
            print(f"   ARN: {instance.get('Arn')}")
            print(f"   Estado: {instance.get('InstanceStatus')}")
            print(f"   Tipo: {instance.get('ServiceRole', 'N/A')}")
            if instance.get('CreatedTime'):
                created = instance['CreatedTime'].strftime('%Y-%m-%d %H:%M:%S UTC')
                print(f"   Creada: {created}")
            print()

    def print_instance_details(self, instance_id: str, details: Dict):
        """Imprime detalles completos de una instancia"""
        self.print_separator(f"🔍 DETALLES DE INSTANCIA: {instance_id}")
        
        if not details:
            print("❌ No se pudieron obtener detalles")
            return
            
        print(f"Alias: {details.get('InstanceAlias', 'N/A')}")
        print(f"ID: {details.get('Id')}")
        print(f"ARN: {details.get('Arn')}")
        print(f"Estado: {details.get('InstanceStatus')}")
        print(f"Tipo identidad: {details.get('IdentityManagementType')}")
        print(f"Llamadas entrantes: {'✅ Habilitadas' if details.get('InboundCallsEnabled') else '❌ Deshabilitadas'}")
        print(f"Llamadas salientes: {'✅ Habilitadas' if details.get('OutboundCallsEnabled') else '❌ Deshabilitadas'}")
        
        if details.get('InstanceAccessUrl'):
            print(f"URL de acceso: {details['InstanceAccessUrl']}")

    def print_queues_summary(self, instance_id: str, queues: List[Dict]):
        """Imprime resumen de colas"""
        self.print_separator(f"📞 COLAS - Instancia: {instance_id}")
        
        if not queues:
            print("❌ No se encontraron colas")
            return
            
        print(f"Total de colas: {len(queues)}\n")
        
        for i, queue in enumerate(queues, 1):
            print(f"{i}. {queue.get('Name')}")
            print(f"   ID: {queue.get('Id')}")
            print(f"   ARN: {queue.get('Arn')}")
            print(f"   Tipo: {queue.get('QueueType', 'N/A')}")
            print()

    def print_users_summary(self, instance_id: str, users: List[Dict]):
        """Imprime resumen de usuarios/agentes"""
        self.print_separator(f"👥 USUARIOS/AGENTES - Instancia: {instance_id}")
        
        if not users:
            print("❌ No se encontraron usuarios")
            return
            
        print(f"Total de usuarios: {len(users)}\n")
        
        for i, user in enumerate(users, 1):
            print(f"{i}. {user.get('Username')}")
            print(f"   ID: {user.get('Id')}")
            print(f"   ARN: {user.get('Arn')}")
            print()

    def print_contact_flows_summary(self, instance_id: str, flows: List[Dict]):
        """Imprime resumen de flujos de contacto"""
        self.print_separator(f"🔄 FLUJOS DE CONTACTO - Instancia: {instance_id}")
        
        if not flows:
            print("❌ No se encontraron flujos de contacto")
            return
            
        print(f"Total de flujos: {len(flows)}\n")
        
        # Agrupar por tipo
        flows_by_type = {}
        for flow in flows:
            flow_type = flow.get('ContactFlowType', 'UNKNOWN')
            if flow_type not in flows_by_type:
                flows_by_type[flow_type] = []
            flows_by_type[flow_type].append(flow)
        
        for flow_type, type_flows in flows_by_type.items():
            print(f"📋 {flow_type} ({len(type_flows)} flujos):")
            for flow in type_flows:
                status = flow.get('ContactFlowState', 'N/A')
                status_icon = '✅' if status == 'ACTIVE' else '❌'
                print(f"   {status_icon} {flow.get('Name')}")
            print()

    def print_phone_numbers_summary(self, instance_id: str, numbers: List[Dict]):
        """Imprime resumen de números de teléfono"""
        self.print_separator(f"📱 NÚMEROS DE TELÉFONO - Instancia: {instance_id}")
        
        if not numbers:
            print("❌ No se encontraron números de teléfono")
            return
            
        print(f"Total de números: {len(numbers)}\n")
        
        for i, number in enumerate(numbers, 1):
            print(f"{i}. {number.get('PhoneNumber')}")
            print(f"   ID: {number.get('PhoneNumberId')}")
            print(f"   ARN: {number.get('PhoneNumberArn')}")
            print(f"   Tipo: {number.get('PhoneNumberType')}")
            print(f"   País: {number.get('PhoneNumberCountryCode')}")
            print()

    def print_hours_of_operations_summary(self, instance_id: str, hours: List[Dict]):
        """Imprime resumen de horarios de operación"""
        self.print_separator(f"🕐 HORARIOS DE OPERACIÓN - Instancia: {instance_id}")
        
        if not hours:
            print("❌ No se encontraron horarios de operación")
            return
            
        print(f"Total de horarios: {len(hours)}\n")
        
        for i, hour in enumerate(hours, 1):
            print(f"{i}. {hour.get('Name')}")
            print(f"   ID: {hour.get('Id')}")
            print(f"   ARN: {hour.get('Arn')}")
            print()

    def export_to_json(self, data: Dict, filename: str = None):
        """Exporta los datos a un archivo JSON"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"amazon_connect_config_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            print(f"✅ Configuración exportada a: {filename}")
        except Exception as e:
            print(f"❌ Error exportando configuración: {e}")

    def review_complete_configuration(self, export_json: bool = False):
        """Revisa y muestra la configuración completa de todas las instancias"""
        print("🔍 Iniciando revisión completa de Amazon Connect...")
        print(f"Región: {self.region}")
        print(f"Timestamp: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        # Obtener instancias
        instances = self.get_instances()
        self.print_instances_summary(instances)
        
        if not instances:
            print("❌ No hay instancias para revisar")
            return
        
        # Datos para exportación
        export_data = {
            'review_timestamp': datetime.now(timezone.utc).isoformat(),
            'region': self.region,
            'instances': []
        }
        
        # Revisar cada instancia en detalle
        for instance in instances:
            instance_id = instance.get('Id')
            if not instance_id:
                continue
                
            print(f"\n🔄 Analizando instancia: {instance.get('InstanceAlias', instance_id)}")
            
            # Obtener toda la información de la instancia
            instance_data = {
                'summary': instance,
                'details': self.get_instance_details(instance_id),
                'queues': self.get_queues(instance_id),
                'users': self.get_users(instance_id),
                'contact_flows': self.get_contact_flows(instance_id),
                'phone_numbers': self.get_phone_numbers(instance_id),
                'hours_of_operations': self.get_hours_of_operations(instance_id)
            }
            
            # Mostrar información detallada
            self.print_instance_details(instance_id, instance_data['details'])
            self.print_queues_summary(instance_id, instance_data['queues'])
            self.print_users_summary(instance_id, instance_data['users'])
            self.print_contact_flows_summary(instance_id, instance_data['contact_flows'])
            self.print_phone_numbers_summary(instance_id, instance_data['phone_numbers'])
            self.print_hours_of_operations_summary(instance_id, instance_data['hours_of_operations'])
            
            export_data['instances'].append(instance_data)
        
        # Resumen final
        self.print_separator("📊 RESUMEN FINAL")
        print(f"Total de instancias: {len(instances)}")
        total_queues = sum(len(inst['queues']) for inst in export_data['instances'])
        total_users = sum(len(inst['users']) for inst in export_data['instances'])
        total_flows = sum(len(inst['contact_flows']) for inst in export_data['instances'])
        total_numbers = sum(len(inst['phone_numbers']) for inst in export_data['instances'])
        
        print(f"Total de colas: {total_queues}")
        print(f"Total de usuarios: {total_users}")
        print(f"Total de flujos: {total_flows}")
        print(f"Total de números: {total_numbers}")
        
        # Exportar si se solicita
        if export_json:
            self.export_to_json(export_data)
        
        print("\n✅ Revisión completada exitosamente")


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Revisa la configuración de Amazon Connect',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Revisión básica
  python amazon_connect_review.py

  # Especificar región
  python amazon_connect_review.py --region us-west-2

  # Usar un perfil AWS específico
  python amazon_connect_review.py --profile mi-perfil

  # Exportar configuración a JSON
  python amazon_connect_review.py --export-json

  # Revisión completa con exportación
  python amazon_connect_review.py --region us-west-2 --profile mi-perfil --export-json

Variables de entorno:
  AWS_PROFILE: Perfil AWS a usar
  AWS_REGION: Región AWS
        """
    )
    
    parser.add_argument(
        '--region', 
        default='us-east-1',
        help='Región AWS (default: us-east-1)'
    )
    
    parser.add_argument(
        '--profile',
        help='Perfil AWS a usar'
    )
    
    parser.add_argument(
        '--export-json',
        action='store_true',
        help='Exportar configuración a archivo JSON'
    )
    
    args = parser.parse_args()
    
    try:
        # Crear reviewer
        reviewer = AmazonConnectReviewer(
            region_name=args.region,
            profile_name=args.profile
        )
        
        # Revisar configuración completa
        reviewer.review_complete_configuration(export_json=args.export_json)
        
    except KeyboardInterrupt:
        print("\n❌ Operación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()