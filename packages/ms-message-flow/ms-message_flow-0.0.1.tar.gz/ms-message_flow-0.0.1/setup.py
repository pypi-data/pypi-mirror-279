import setuptools

setuptools.setup(
    name="ms-message_flow",
    version="0.0.1",
    author="Cayo Slowik",
    author_email="cayo.slowik@brf.com",
    description="Sistema de envio de mensagens",
    url="https://dev.azure.com/brf-corp/Analytics-DataScience/_git/analytics-message-flow",
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "msal",
        "requests",
        "pymsteams",
        "urllib3"
    ],
)
