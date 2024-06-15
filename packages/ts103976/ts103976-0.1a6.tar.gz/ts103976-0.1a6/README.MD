# TS 103 976 Demonstration Implementation

This repo contains a python package for creating and parsing messages as per ETSI TS 103 976.

It is intended for test and demonstration purposes only. It should not be used for production purposes. Any use is entirely at the users risk.

## Getting Started

Install the package using pip

```
#> pip install ts103976
```

## LEA side

### Usage

The package provides a simple CLI app for creating the JSON for VINToCommsID requests

```
#> lea -h

usage: lea [-h] [-s SENDERCC] [-u SENDERID] [-r RECEIVERCC] [-i RECEIVERID] [-t TASKREF] [-v VIN] [-d DELIVERYURL]

Generates JSON messages for simple example requests following TS 103 976, encapsulated in TS 103 120. This is an example implementation for testing and demonstration purposes, and should not be used in production environments.

options:
  -h, --help            show this help message and exit
  -s SENDERCC, --sendercc SENDERCC
                        Sender Country Code used in the TS 103 120 header
  -u SENDERID, --senderid SENDERID
                        Sender Unique ID used in the TS 103 120 header
  -r RECEIVERCC, --receivercc RECEIVERCC
                        Receiver Country Code used in the TS 103 120 header
  -i RECEIVERID, --receiverid RECEIVERID
                        Receiver Unique ID used in the TS 103 120 header
  -t TASKREF, --taskref TASKREF
                        Task Reference (LDID) used in the TS 103 120 LDTaskRequest
  -v VIN, --vin VIN     VIN to query as a RequestValue in the TS 103 120 LDTaskRequest
  -d DELIVERYURL, --deliveryurl DELIVERYURL
                        Delivery URL included in the TS 103 120 LDTaskRequest, as a destination for results
```

### Examples

To create a request for a particular VIN:

```
#> lea --vin 1G9Y817H34LSP7293
```

Use e.g. the HTTPIE library to send the request directly to a TS 103 120 endpoint

```
#> lea | http POST https://example.com/103120/
```

Pipe the output directly to the RPS tool (see below). The TS 103 120 response will be returned by the rps tool. You need to specify a delivery address in the lea tool (--deliverurl) or a default delivery behaviour in the rps tool (--delivery) in order to actually see the result set.

```
#> lea | rps
```


## RPS side

### Usage

The rps tool accepts a TS 103 120 request message containing one or more LDTaskRequests with parameters as specified in TS 103 976 for simple vehicle requests. Currently only VINtoCommsID is supported.


```
#> rps -h

usage: rps [-h] [-r RECEIVERCC] [-i RECEIVERID] [-a ALLOWANYID]
           [-d {skipdelivery,fail,delivertodefault,writetostdout,writetostderr}]
           [--defaultaddress DEFAULTADDRESS] [-j INPUT] [-v]

Responds to JSON messages for simple example requests following TS 103 976, encapsulated in TS    
103 120, and produces simple example responses. TS 103 120 response messages will be written to   
stdout. The DELIVER message containing any results will either be set to the delivery address     
specified in the LDTaskRequest or written to disk This is an example implementation for testing   
and demonstration purposes, and should not be used in production environments.

options:
  -h, --help            show this help message and exit
  -r RECEIVERCC, --receivercc RECEIVERCC
                        Receiver Country Code for the TS 103 120 receiver. Messages with other Receiver Country Code values will be rejected unless the '--allowanyid' flag is set.
  -i RECEIVERID, --receiverid RECEIVERID
                        Receiver Unique ID for the TS 103 120 receiver. Messages with other Receiver Unique ID values will be rejected unless the '--allowanyid' flag is set.
  -a ALLOWANYID, --allowanyid ALLOWANYID
                        Respond to messages to any Receiver ID, regardless of the values set by '--receivercc' or '--receiverid'.
  -d {skipdelivery,fail,delivertodefault,writetostdout,writetostderr}, --delivery {skipdelivery,fail,delivertodefault,writetostdout,writetostderr}
                        Behaviour if a request does not specify a delivery address
  --defaultaddress DEFAULTADDRESS
                        Default delivery address. Implies --delivery delivertodefault
  -j INPUT, --input INPUT
                        Path to input file (if absent, stdin is used)
  -v, --verbose         Verbosity. Can be specified multiple times for extra verbosity

```

### Examples

Wait for input on stdin, write the TS 103120-layer response on stdin. If a delivery destination is given in the request (e.g. lea --deliveryurl) then send the results there, otherwise do nothing.

```
#> rps
```

Wait for input on stdin. Write the immediate response to stdout, and the DELIVER request containing the results to stderr unless a delivery URL is specified in the request. Capture both messages to json files.

```
#> rps -d writetostderr >response.json 2&>deliver_results.json
```