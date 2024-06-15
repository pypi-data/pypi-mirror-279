# Vault Keyring Client

This project provides an installable version of the original community script `vault-keyring-client.py` for Ansible, allowing you to manage vault passwords using your OS's native keyring application.

## Description

The `vault-keyring-client` is a CLI tool to store and retrieve Ansible vault passwords in the keyring. This version is implemented using `typer` for a modern CLI interface, making it easy to use and extend.

## Installation

To install the `vault-keyring-client`, you can use [Poetry](https://python-poetry.org/):

```sh
poetry add git+https://git@github.com/jakob1379/vault-keyring-client.git#main
```

## Usage

```console
$ vault-keyring-client [OPTIONS]
```

**Options**:

* `--vault-id TEXT`: Name of the vault secret to get from keyring.
* `--username TEXT`: The username whose keyring is queried.
* `--set`: Set the password instead of getting it.
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

## Original Script

This project is based on the original `vault-keyring-client.py` script contributed by Matt Martz and Justin Mayer. The original script can be found in the Ansible Community's contrib-scripts repository:

[Original vault-keyring-client.py script](https://github.com/ansible-community/contrib-scripts/blob/main/vault/vault-keyring-client.py)

## Using with Ansible

The script is designed to work with Ansible, making your playbooks more efficient by eliminating the need to manually enter `become_pass` for each host. Follow these steps to set it up:

1. **Create an Entry**:
   First, create an entry with `vault-keyring-client --set --vault-id my_vault_id`.

2. **Configure Ansible**:
   To make Ansible automatically try the passwords stored in your keyring, add the following to your `.envrc` or manually source your `.env` file:
   ```bash
   export ANSIBLE_VAULT_IDENTITY_LIST="my_vault_id@$(poetry run which vault-keyring-client),my_other_vault_id@$(poetry run which vault-keyring-client)"
   ```

3. **Create a Secure Vault**:
   Create a vault file outside of your repository to avoid accidental commits. Store it in a safe location, for example, `~/.become_passwords`. Structure the key-value pairs as `become_pass_<hostname>: "mytopsecret_host_password"`. Encrypt the file using:
   ```sh
   ansible-vault encrypt --encrypt-vault-id my_vault_id <path_to_vault>
   ```

4. **Update Playbooks**:
   Add the following configuration to your playbooks to use the stored passwords:
   ```yml
   - name: Playbook that does not require manual sudo passwords
     hosts: amazing_host
     become: true
     vars:
       ansible_become_password: "{{ lookup('vars', 'become_pass_' + inventory_hostname) }}"
     vars_files:
       - ~/.become_passwords.yml
     roles:
       - users
   ```
   When you run the playbook, Ansible will try all keys in the `VAULT_IDENTITY_LIST` in order and use the correct one to unlock `~/.become_passwords`, matching the password with the hostname.

## License

This project is licensed under the GNU General Public License v3.0 or later. See the [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) file for details.
