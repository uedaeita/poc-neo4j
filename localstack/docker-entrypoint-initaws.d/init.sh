#!/usr/bin/env bash

set -euo pipefail

# localstackの設定
readonly ENDPOINT_URL=http://localhost:4566
readonly PROJECT_ID=000000000000
# S3は既存バケットがあるとコマンドエラーとなるので比較用に既存バケット一覧を用意しておく
readonly EXISTING_BUCKETS=(`aws --endpoint-url=${ENDPOINT_URL} s3 ls s3:// | awk '{print $3}'`)

# Utils
#------------------------------------------------
make_buckets_if_not_exist() {
    for bucket_name in "$@"; do
        if ! [[ " ${EXISTING_BUCKETS[@]} " =~ " ${bucket_name} " ]]; then
            aws --endpoint-url=${ENDPOINT_URL} s3 mb s3://${bucket_name}
        else
            echo "[warn] skipped making the s3 bucket: $bucket_name already exists"
        fi
    done
}

make_sns_topics() {
    for topic_name in "$@"; do
        aws --endpoint-url=${ENDPOINT_URL} sns create-topic --name ${topic_name}
    done
}

make_sqs_queues() {
    for queue_name in "$@"; do
        aws --endpoint-url=${ENDPOINT_URL} sqs create-queue --queue-name ${queue_name}
    done
}

subscribe_queue_to_topic() {
    local _queue_name="$1"
    local _topic_name="$2"
    aws --endpoint-url=${ENDPOINT_URL} sns subscribe \
        --topic-arn arn:aws:sns:${DEFAULT_REGION}:${PROJECT_ID}:${_topic_name} \
        --protocol sqs \
        --notification-endpoint ${ENDPOINT_URL}/${PROJECT_ID}/${_queue_name}
}

# Initializing resources
#------------------------------------------------
make_graphdb_resources() {
    make_buckets_if_not_exist xaion-neo4j-csv
}

# Main
#------------------------------------------------
main() {
    echo "[info] START: initializing resources for localstack"

    make_graphdb_resources

    echo "[info] DONE : initializing resources for localstack"
}

main
