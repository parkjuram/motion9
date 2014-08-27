from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, settings
import random

REPO_URL = 'https://github.com/parkjuram/motion9'

USER_NAME = "arsdale"
PROJECT_NAME = "motion9"

env.hosts = ['175.126.82.107']
env.user = 'CREATE DATABASE '
# env.key_filename = '/Users/John/.ssh/google_compute_engine'
env.forward_agent = True

def deploy():
    project_folder = '/home/%s/project/%s' % ( USER_NAME, PROJECT_NAME )
    source_folder = project_folder + '/source'

    _create_directory_structure_if_necessary( project_folder )
    _get_latest_source( source_folder )
    # _update_settings( source_folder, env.host )
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

def _create_directory_structure_if_necessary( project_folder ):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % ( project_folder, subfolder ) )

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % (source_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))

def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/motion9/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s"]' % (site_name,)
    )
    secret_key_file = source_folder + '/motion9/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (
            virtualenv_folder, source_folder
    ))

def _update_static_files(source_folder):
    run('cd %s && sudo ../virtualenv/bin/python manage.py collectstatic --noinput' % (
        source_folder,
    ))

def _update_database(source_folder):
    run('cd %s && sudo ../virtualenv/bin/python manage.py syncdb --noinput' % (source_folder,))

    with settings(warn_only=True):
        # # run('cd %s && ../virtualenv/bin/python manage.py schemamigration users --initial' % (source_folder,))
        run('cd %s && sudo ../virtualenv/bin/python manage.py schemamigration users --auto' % (source_folder,))
        run('cd %s && sudo ../virtualenv/bin/python manage.py migrate users' % (source_folder,))
        #
        # run('cd %s && ../virtualenv/bin/python manage.py schemamigration web --initial' % (source_folder,))
        run('cd %s && sudo ../virtualenv/bin/python manage.py schemamigration web --auto' % (source_folder,))
        run('cd %s && sudo ../virtualenv/bin/python manage.py migrate web' % (source_folder,))

        # run('cd %s && ../virtualenv/bin/python manage.py schemamigration foradmin --initial' % (source_folder,))
        run('cd %s && sudo ../virtualenv/bin/python manage.py schemamigration foradmin --auto' % (source_folder,))
        run('cd %s && sudo ../virtualenv/bin/python manage.py migrate foradmin' % (source_folder,))
        #
        # # run('cd %s && ../virtualenv/bin/python manage.py schemamigration foradmin --initial' % (source_folder,))
        # run('cd %s && sudo ../virtualenv/bin/python manage.py schemamigration foradmin --auto' % (source_folder,))
        # run('cd %s && sudo ../virtualenv/bin/python manage.py migrate foradmin' % (source_folder,))

    # one-off fake database migration. remove me before next deploy
    # run('cd %s && ../virtualenv/bin/python manage.py migrate lists --fake 0001' % (
        # source_folder,
    # ))
    # run('cd %s && ../virtualenv/bin/python manage.py migrate' % (source_folder,))