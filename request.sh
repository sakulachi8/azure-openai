
export MY_HOST=https://xxxxxx.azurewebsites.net
export MY_HOST=http://127.0.0.1:8000

curl -X POST "${MY_HOST}/api/messages" -H  "accept: application/json" -H  "Content-Type: application/json" -d '{"messages":[{"role":"user", "content":"est conscient du fait qu’il utilise l’objet."}]}'
