cd ..
waitress-serve --listen=0.0.0.0:5000 --threads=8 --max-request-header-size=1048576 --call flask_entrypoint_casino_cust:create_app