# Handwriting visualizations
- stable version: 0.3.0

# Publishing to pypi
- Easiest way is to be on WSL2 or Linux distro
- Install **poetry**
- Rename file **_Makefile** to **Makefile**
- In the Makefile edit **YOUR_PYPI_TOKEN** with your generated pypi token
- In the same directory as this README file is run commands:
```
make set_token
make publish
```

