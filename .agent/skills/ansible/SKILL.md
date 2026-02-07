---
name: Ansible
description: Playbooks, roles, idempotent configuration
---

# Ansible Skill

## Inventory

```ini
# inventory.ini
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com

[all:vars]
ansible_user=ubuntu
```

## Playbook

```yaml
# playbook.yml
- name: Configure web servers
  hosts: webservers
  become: true
  
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: yes

    - name: Copy config file
      copy:
        src: nginx.conf
        dest: /etc/nginx/nginx.conf
      notify: Restart nginx

  handlers:
    - name: Restart nginx
      service:
        name: nginx
        state: restarted
```

## Commands

```bash
ansible-playbook -i inventory.ini playbook.yml
ansible all -m ping -i inventory.ini
ansible webservers -a "uptime" -i inventory.ini
```

## Roles Structure

```
roles/
└── webserver/
    ├── tasks/main.yml
    ├── handlers/main.yml
    ├── templates/
    ├── files/
    └── vars/main.yml
```

## When to Apply
Use when configuring servers, deploying applications, or automating ops tasks.
