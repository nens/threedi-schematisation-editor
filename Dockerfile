from qgis/qgis:release-3_22
RUN apt-get update && apt-get install -y python3-pyqt5.qtwebsockets && apt-get clean
RUN pip3 install pytest
RUN pip3 install 'coverage>5' --force
RUN pip3 install pytest-cov
RUN qgis_setup.sh 