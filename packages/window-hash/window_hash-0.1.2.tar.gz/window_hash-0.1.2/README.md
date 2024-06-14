# Introduction

This library provides a simple wrapper to help divide a stream of items into pages/windows, with hash value calculated for each window as checksum and/or identifier.

It supports all hash functions from standard library's `hashlib`.

It supports any condition to help determine when a window is complete. In addition, a few common conditions are provided as well, based on window size or duration. Examples:
- Publishing to a message queue with total size limitation for each message
- Publishing to a message queue where each message is for items of each minute
