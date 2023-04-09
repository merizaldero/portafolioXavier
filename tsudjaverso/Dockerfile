FROM mono:4.6.2.16

RUN curl http://dist.opensimulator.org/opensim-0.9.0.0-rc1.tar.gz -s | tar xzf -
mv /opensim-0.9.0.0-rc1 /opensimulator
COPY Regions.ini /regions/Regions.ini
COPY OpenSim.ini /opensimulator/bin/OpenSim.ini
COPY StandaloneCommon.ini /opensimulator/bin/config-include/StandaloneCommon.ini
COPY osslEnable.ini /opensimulator/bin/config-include/osslEnable.ini
EXPOSE 9000
WORKDIR /opensimulator/bin

CMD [ "mono",  "./OpenSim.exe" ]
