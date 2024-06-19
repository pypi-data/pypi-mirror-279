from raft.tasks import task
from convocations.base.utils import notice, notice_end, print_table
from convocations.aws.base import AwsTask, yielder


@task(klass=AwsTask)
def managed_instances(ctx, name='', session=None, **kwargs):
    """
    lists all ssm managed instances with `name` in their `ComputerName`
    """
    name = name.lower()
    notice('connecting to ssm')
    ssm = session.client('ssm')
    notice_end()
    notice('getting instance information')
    rg = yielder(ssm, 'describe_instance_information', session)
    header = [ 'id', 'name', 'ip' ]
    rows = []
    for x in rg:
        st = x['ComputerName']
        instance_id = x['InstanceId']
        if name in st.lower():
            row = [ instance_id, st, x['IPAddress'] ]
            rows.append(row)
    notice_end()
    rows.sort(key=lambda lx: lx[1])
    print()
    print_table(header, rows)


@task(klass=AwsTask)
def unmanaged_instances(ctx, session=None, **kwargs):
    """
    lists all ec2 instances not enrolled in ssm management
    """
    from convocations.aws.base import name_tag
    from convocations.aws.ec2 import yield_instances
    notice('connecting to ssm')
    ssm = session.client('ssm')
    notice_end()
    notice('getting instance information')
    rg = yielder(ssm, 'describe_instance_information', session)
    managed_ids = { x['InstanceId'] for x in rg }
    notice_end()
    notice('connecting to ec2')
    instances = yield_instances(session=session)
    instances = [ x for x in instances if x['InstanceId'] not in managed_ids ]
    notice_end()
    header = [ 'id', 'name', 'ip' ]
    rows = []
    for x in instances:
        row = [ x['InstanceId'], name_tag(x), x.get('PrivateIpAddress', '') ]
        rows.append(row)
    rows.sort(key=lambda lx: lx[1])
    print()
    print_table(header, rows)
