"""Upload static output with a dedicated SSH key and a pinned server host key."""
import os
from pathlib import Path
import subprocess
import tempfile


def quote(value):
    if any(c in value for c in ('\n', '\r', '\x00')):
        raise ValueError('Control characters are not allowed in SFTP paths')
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def main():
    host = os.environ['SSH_HOST']
    port = os.environ['SSH_PORT']
    user = os.environ['SSH_USER']
    destination = os.environ.get('SSH_DIRECTORY', '').strip()
    if host != '92.113.28.123' or port != '65002' or user != 'u509134529':
        raise ValueError('Connection settings must match the verified Hostinger account')
    if not destination.startswith('/') or destination in ('/', '/home', '/home/u509134529'):
        raise ValueError('Set HOSTINGER_SSH_DIRECTORY to the absolute website public_html path')
    if Path(destination).name != 'public_html' or '..' in Path(destination).parts:
        raise ValueError('Deployment destination must be a public_html directory without parent traversal')
    source = Path('dist').resolve()
    if not (source / 'index.html').is_file():
        raise ValueError('Build output is missing; run npm run build first')
    commands = ['cd ' + quote(destination)]
    directories = sorted((p for p in source.rglob('*') if p.is_dir()), key=lambda p: (len(p.parts), str(p)))
    commands += ['-mkdir ' + quote(p.relative_to(source).as_posix()) for p in directories]
    files = sorted((p for p in source.rglob('*') if p.is_file() and not any(part.startswith('.') for part in p.relative_to(source).parts)), key=lambda p: (p.suffix == '.html', str(p)))
    commands += ['put ' + quote(str(p)) + ' ' + quote(p.relative_to(source).as_posix()) for p in files]
    commands.append('bye')
    with tempfile.TemporaryDirectory(prefix='hostinger-deploy-') as directory:
        key = Path(directory) / 'deploy_key'
        key.write_text(os.environ['SSH_PRIVATE_KEY'].strip() + '\n')
        key.chmod(0o600)
        batch = Path(directory) / 'upload.sftp'
        batch.write_text('\n'.join(commands) + '\n')
        print(f'Uploading {len(files)} files over SFTP with verified server identity.', flush=True)
        subprocess.run([
            'sftp', '-F', '/dev/null', '-P', port, '-i', str(key), '-b', str(batch),
            '-o', 'BatchMode=yes', '-o', 'IdentitiesOnly=yes',
            '-o', 'StrictHostKeyChecking=yes',
            '-o', 'UserKnownHostsFile=' + str(Path('.github/hostinger_known_hosts').resolve()),
            '-o', 'HostKeyAlgorithms=ssh-ed25519',
            '-o', 'ConnectTimeout=15', '-o', 'ConnectionAttempts=1',
            '-o', 'ServerAliveInterval=15', '-o', 'ServerAliveCountMax=2',
            user + '@' + host,
        ], check=True, timeout=180)
    print('Upload complete. Existing remote files and .htaccess were preserved.', flush=True)


if __name__ == '__main__':
    main()
