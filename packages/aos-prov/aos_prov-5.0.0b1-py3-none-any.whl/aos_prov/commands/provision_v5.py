from aos_prov.utils.config import Config
from aos_prov.communication.unit.v5.unit_communication_v5 import UnitCommunicationV5
from aos_prov.utils.common import generate_random_password, print_message
from aos_prov.communication.cloud.cloud_api import CloudAPI

def  run_provision_v5(config: Config, unit_address: str, cloud_api: CloudAPI):
    unit_communication = UnitCommunicationV5(unit_address)
    unit_communication.get_all_node_ids()

    for node_id in config.node_ids:
        password = generate_random_password()
        config.add_node_password(node_id, password)
        unit_communication.start_provisioning(node_id, password)
        config.supported_cert_types = unit_communication.get_cert_types()

        for cert_type in config.supported_cert_types:
            config.add_node_certificates(node_id, unit_communication.create_keys(cert_type, password, node_id))

    register_payload = {
        'hardware_id': config.system_id,
        'system_uid': config.system_id,
        'model_name': config.model_name,
        'model_version': config.model_version,
        'provisioning_software': 'aos-provisioning:3.1',
        'additional_csrs': [],
    }

    for node, node_csrs in config.node_certificates:
        for csr_cert in node_csrs:
            if csr_cert.cert_type == 'online':
                register_payload['online_public_csr'] = csr_cert.csr
                if csr_cert.node_id:
                    register_payload['online_public_node_id'] = csr_cert.node_id
            elif csr_cert.cert_type == 'offline':
                register_payload['offline_public_csr'] = csr_cert.csr
                if csr_cert.node_id:
                    register_payload['offline_public_node_id'] = csr_cert.node_id
            else:
                register_payload['additional_csrs'].append({
                    'cert_type': csr_cert.cert_type,
                    'csr': csr_cert.csr,
                    'node_id': csr_cert.node_id,
                })

    response = cloud_api.register_device(register_payload)
    system_uid = response.get('system_uid')
    additional_certs = response.get('additional_certs', [])

    for node_id, cert in config.node_certificates:
        if cert.cert_type == 'online':
            cert.certificate = response.get('online_certificate')
        elif cert.cert_type == 'offline':
            cert.certificate = response.get('offline_certificate')
        else:
            for additional_cert in additional_certs:
                if additional_cert['cert_type'] == cert.cert_type:
                    if additional_cert.get('node_id'):
                        if additional_cert.get('node_id') == cert.node_id:
                            cert.certificate = additional_cert['cert']
                            break
                    else:
                        cert.certificate = additional_cert['cert']
                        cert.node_id = additional_cert.get('node_id')
                        break

    for node_id, apply_certs in config.node_certificates:
        for cert in apply_certs:
            unit_communication.apply_certificate(cert)

    for node_id in config.node_ids:
        unit_communication.finish_provisioning(node_id, config.node_password[node_id])

    print_message('[green]Finished successfully!')
    link = cloud_api.get_unit_link_by_system_uid(system_uid)

    if link:
        print_message(f'You may find your unit on the cloud here: [green]{link}')
