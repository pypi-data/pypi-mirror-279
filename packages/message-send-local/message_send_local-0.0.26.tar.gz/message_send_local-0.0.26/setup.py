"""imports"""
import setuptools

PACKAGE_NAME = "message-send-local"
# Since all PACAKGE_NAMEs are with an underscore, we don't need this. Why do we need it?
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.26',  # https://pypi.org/project/message-send-local/
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles message_send_local Python",
    long_description="PyPI Package for Circles message_send_local Python",
    long_description_content_type='text/markdown',
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-local-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    # TODO Shall we add language-remote here?
    install_requires=[
        'database-mysql-local>=0.0.290',
        'message-local>=0.0.123', # TODO Can we remove it as it is included in messages-local?
        'messages-local>=0.0.49',
        'logger-local>=0.0.135'
    ],
)
