import re
from fabric.api import env, run, hide, task
from envassert import detect, file, port, process, service, user
from hot.utils.test import get_artifacts


def app_is_responding():
    with hide('running', 'stdout'):
        homepage = run("curl http://localhost")
        if re.search('You may have mistyped the address', homepage):
            return True
        else:
            return False


@task
def check():
    env.platform_family = detect.detect()

    assert file.exists('/home/rails/railsapp/current/config/database.yml'), \
        '/home/rails/railsapp/current/config/database.yml did not exist'

    assert port.is_listening(80), 'port 80/nginx is not listening'
    assert port.is_listening(3306), 'port 3306/mysqld is not listening'

    assert user.exists('mysql'), 'mysql user does not exist'
    assert user.exists('rails'), 'rails user does not exist'

    assert process.is_up('ruby'), 'unicorn is not running'
    assert process.is_up('nginx'), 'nginx is not running'
    assert process.is_up('mysqld'), 'mysqld is not running'

    assert service.is_enabled('nginx'), 'nginx service not enabled'
    assert service.is_enabled('mysql'), 'mysql service not enabled'
    assert service.is_enabled('unicorn'), 'unicorn service not enabled'

    assert app_is_responding(), 'Rails app did not respond as expected.'


@task
def artifacts():
    env.platform_family = detect.detect()
    get_artifacts()
