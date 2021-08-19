#!/bin/bash
read -p "Enter your username(email): " email
read -s -p "Enter Password: "  password

echo "email: $email" > cred.yml
echo "password: $password" >> cred.yml