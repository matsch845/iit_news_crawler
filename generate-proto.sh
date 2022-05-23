#!/bin/bash

protoc --proto_path=proto --python_out=build/gen proto/article.proto
