#!/usr/bin/env bash

aws apigateway get-model --rest-api-id jw68bdy2t5 --model-name Response | jq --raw-output '.schema' > ./assets/vehicle/response.schema.json
aws apigateway get-model --rest-api-id 2bzr9vm131 --model-name Response | jq --raw-output '.schema' > ./assets/transport/response.schema.json

aws apigateway get-model --rest-api-id 24ut7ue8d8 --model-name APIStorageStatusRequest | jq --raw-output '.schema' > ./assets/storage-and-hook/APIStorageStatusRequest.schema.json
aws apigateway get-model --rest-api-id 24ut7ue8d8 --model-name CreateHookRequest | jq --raw-output '.schema' > ./assets/storage-and-hook/CreateHookRequest.schema.json
aws apigateway get-model --rest-api-id 24ut7ue8d8 --model-name EventsResponse | jq --raw-output '.schema' > ./assets/storage-and-hook/EventsResponse.schema.json
aws apigateway get-model --rest-api-id 24ut7ue8d8 --model-name Hook | jq --raw-output '.schema' > ./assets/storage-and-hook/Hook.schema.json
aws apigateway get-model --rest-api-id 24ut7ue8d8 --model-name Hooks | jq --raw-output '.schema' > ./assets/storage-and-hook/Hooks.schema.json
aws apigateway get-model --rest-api-id 24ut7ue8d8 --model-name OKResponse | jq --raw-output '.schema' > ./assets/storage-and-hook/OKResponse.schema.json
aws apigateway get-model --rest-api-id 24ut7ue8d8 --model-name StorageStatusResponse | jq --raw-output '.schema' > ./assets/storage-and-hook/StorageStatusResponse.schema.json
aws apigateway get-model --rest-api-id 24ut7ue8d8 --model-name UpdateHookRequest | jq --raw-output '.schema' > ./assets/storage-and-hook/UpdateHookRequest.schema.json

for file in $(find ./assets/storage-and-hook -name '*.json'); do
    # replace the remote reference with the local one
    sed -i 's|https://apigateway.amazonaws.com/restapis/'"24ut7ue8d8"'/models/\(.*\)"|\1.schema.json"|g' "$file"
done