#!/usr/bin/env python

#
# Generated Mon Jan 22 10:52:36 2018 by generateDS.py version 2.29.5.
# Python 3.6.3 (default, Oct  6 2017, 08:44:35)  [GCC 5.4.0 20160609]
#
# Command line options:
#   ('-f', '')
#   ('-a', 'xsi:')
#   ('--super', 'domainservice')
#   ('-o', 'domainservice.py')
#   ('-s', 'subdomainservice.py')
#
# Command line arguments:
#   /opt/infa/pwc/1020/shared/bin/com.informatica.isp.metadata.domainservice.xsd
#
# Command line:
#   /home/arthur/.virtualenvs/octopus-tentacle/bin/generateDS.py -f -a "xsi:" --super="domainservice" -o "domainservice.py" -s "subdomainservice.py" /opt/infa/pwc/1020/shared/bin/com.informatica.isp.metadata.domainservice.xsd
#
# Current working directory (os.getcwd()):
#   tests
#

import sys
from lxml import etree as etree_

from octopus.common import domainservice as supermod


def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        parser = etree_.ETCompatXMLParser()
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

#
# Globals
#

ExternalEncoding = 'utf-8'

#
# Data representation classes
#


class DBConnectivitySub(supermod.DBConnectivity):
    def __init__(self, id=None, idref=None, iid=None, dbConnectString=None, dbEncryptedPassword=None, dbHost=None, dbName=None, dbPort=None, dbSchema=None, dbTLSEnabled=None, dbTableSpace=None, dbTruststoreLocation=None, dbType=None, dbUsername=None, trustedConnection=None, truststorePassword=None, annotations=None):
        super(DBConnectivitySub, self).__init__(id, idref, iid, dbConnectString, dbEncryptedPassword, dbHost, dbName, dbPort, dbSchema, dbTLSEnabled, dbTableSpace, dbTruststoreLocation, dbType, dbUsername, trustedConnection, truststorePassword, annotations, )
supermod.DBConnectivity.subclass = DBConnectivitySub
# end class DBConnectivitySub


class EarlierInfaHomeConfigSub(supermod.EarlierInfaHomeConfig):
    def __init__(self, id=None, idref=None, iid=None, earlierInfaHome=None, earlierInfaHomeVersion=None, earlierJavaHome=None, annotations=None):
        super(EarlierInfaHomeConfigSub, self).__init__(id, idref, iid, earlierInfaHome, earlierInfaHomeVersion, earlierJavaHome, annotations, )
supermod.EarlierInfaHomeConfig.subclass = EarlierInfaHomeConfigSub
# end class EarlierInfaHomeConfigSub


class HttpsInfoSub(supermod.HttpsInfo):
    def __init__(self, id=None, idref=None, iid=None, encryptedKeystorePass=None, httpsPort=None, keystoreFile=None, annotations=None):
        super(HttpsInfoSub, self).__init__(id, idref, iid, encryptedKeystorePass, httpsPort, keystoreFile, annotations, )
supermod.HttpsInfo.subclass = HttpsInfoSub
# end class HttpsInfoSub


class NodeSamlConfigSub(supermod.NodeSamlConfig):
    def __init__(self, id=None, idref=None, iid=None, assertionSigningCertificateAlias=None, samlEnabled=None, samlTrustStore=None, samlTrustStorePassword=None, annotations=None):
        super(NodeSamlConfigSub, self).__init__(id, idref, iid, assertionSigningCertificateAlias, samlEnabled, samlTrustStore, samlTrustStorePassword, annotations, )
supermod.NodeSamlConfig.subclass = NodeSamlConfigSub
# end class NodeSamlConfigSub


class SecurityConfigSub(supermod.SecurityConfig):
    def __init__(self, id=None, idref=None, iid=None, ciphers=None, kerberosEnabled=None, keystore=None, keystorePassword=None, nodeUserAccount=None, secretKeysDirectory=None, serviceRealmName=None, siteKeyHashValue=None, trustStore=None, trustStorePassword=None, userRealmName=None, annotations=None, nodeSamlConfig=None):
        super(SecurityConfigSub, self).__init__(id, idref, iid, ciphers, kerberosEnabled, keystore, keystorePassword, nodeUserAccount, secretKeysDirectory, serviceRealmName, siteKeyHashValue, trustStore, trustStorePassword, userRealmName, annotations, nodeSamlConfig, )
supermod.SecurityConfig.subclass = SecurityConfigSub
# end class SecurityConfigSub


class ServiceProcessStartupStateSub(supermod.ServiceProcessStartupState):
    def __init__(self, id=None, idref=None, iid=None, domainNode=None, serviceName=None, state=None, annotations=None):
        super(ServiceProcessStartupStateSub, self).__init__(id, idref, iid, domainNode, serviceName, state, annotations, )
supermod.ServiceProcessStartupState.subclass = ServiceProcessStartupStateSub
# end class ServiceProcessStartupStateSub


class ServiceStartupStateSub(supermod.ServiceStartupState):
    def __init__(self, id=None, idref=None, iid=None, operationMode=None, serviceName=None, state=None, annotations=None):
        super(ServiceStartupStateSub, self).__init__(id, idref, iid, operationMode, serviceName, state, annotations, )
supermod.ServiceStartupState.subclass = ServiceStartupStateSub
# end class ServiceStartupStateSub


class ISPObjectSub(supermod.ISPObject):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, extensiontype_=None):
        super(ISPObjectSub, self).__init__(id, idref, iid, annotations, extensiontype_, )
supermod.ISPObject.subclass = ISPObjectSub
# end class ISPObjectSub


class ISPBooleanSub(supermod.ISPBoolean):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, value=None):
        super(ISPBooleanSub, self).__init__(id, idref, iid, annotations, value, )
supermod.ISPBoolean.subclass = ISPBooleanSub
# end class ISPBooleanSub


class ISPIntegerSub(supermod.ISPInteger):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, value=None):
        super(ISPIntegerSub, self).__init__(id, idref, iid, annotations, value, )
supermod.ISPInteger.subclass = ISPIntegerSub
# end class ISPIntegerSub


class ISPLongSub(supermod.ISPLong):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, value=None):
        super(ISPLongSub, self).__init__(id, idref, iid, annotations, value, )
supermod.ISPLong.subclass = ISPLongSub
# end class ISPLongSub


class ISPNamedObjectSub(supermod.ISPNamedObject):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, name=None, extensiontype_=None):
        super(ISPNamedObjectSub, self).__init__(id, idref, iid, annotations, name, extensiontype_, )
supermod.ISPNamedObject.subclass = ISPNamedObjectSub
# end class ISPNamedObjectSub


class ISPStringSub(supermod.ISPString):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, string=None):
        super(ISPStringSub, self).__init__(id, idref, iid, annotations, string, )
supermod.ISPString.subclass = ISPStringSub
# end class ISPStringSub


class NodeAddressSub(supermod.NodeAddress):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, host=None, httpPort=None, port=None):
        super(NodeAddressSub, self).__init__(id, idref, iid, annotations, host, httpPort, port, )
supermod.NodeAddress.subclass = NodeAddressSub
# end class NodeAddressSub


class NodeRefSub(supermod.NodeRef):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, address=None, nodeName=None):
        super(NodeRefSub, self).__init__(id, idref, iid, annotations, address, nodeName, )
supermod.NodeRef.subclass = NodeRefSub
# end class NodeRefSub


class TimeOfDaySub(supermod.TimeOfDay):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, hourOfDay=None, minutes=None):
        super(TimeOfDaySub, self).__init__(id, idref, iid, annotations, hourOfDay, minutes, )
supermod.TimeOfDay.subclass = TimeOfDaySub
# end class TimeOfDaySub


class IdObjSub(supermod.IdObj):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, name=None, securityDomain=None):
        super(IdObjSub, self).__init__(id, idref, iid, annotations, name, securityDomain, )
supermod.IdObj.subclass = IdObjSub
# end class IdObjSub


class OptionSub(supermod.Option):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, name=None, defaultValue=None, isModified=None, isSensitive=None, type_=None, value=None):
        super(OptionSub, self).__init__(id, idref, iid, annotations, name, defaultValue, isModified, isSensitive, type_, value, )
supermod.Option.subclass = OptionSub
# end class OptionSub


class OptionGroupSub(supermod.OptionGroup):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, name=None, options=None):
        super(OptionGroupSub, self).__init__(id, idref, iid, annotations, name, options, )
supermod.OptionGroup.subclass = OptionGroupSub
# end class OptionGroupSub


class GroupRefSub(supermod.GroupRef):
    def __init__(self):
        super(GroupRefSub, self).__init__()
supermod.GroupRef.subclass = GroupRefSub
# end class GroupRefSub


class SensitiveOptionSub(supermod.SensitiveOption):
    def __init__(self, sensitiveValue=None):
        super(SensitiveOptionSub, self).__init__(sensitiveValue, )
supermod.SensitiveOption.subclass = SensitiveOptionSub
# end class SensitiveOptionSub


class UserRefSub(supermod.UserRef):
    def __init__(self):
        super(UserRefSub, self).__init__()
supermod.UserRef.subclass = UserRefSub
# end class UserRefSub


class annotationsSub(supermod.annotations):
    def __init__(self, anytypeobjs_=None):
        super(annotationsSub, self).__init__(anytypeobjs_, )
supermod.annotations.subclass = annotationsSub
# end class annotationsSub


class IBlobSub(supermod.IBlob):
    def __init__(self, id=None, valueOf_=None):
        super(IBlobSub, self).__init__(id, valueOf_, )
supermod.IBlob.subclass = IBlobSub
# end class IBlobSub


class IBlobsSub(supermod.IBlobs):
    def __init__(self, IBlob=None):
        super(IBlobsSub, self).__init__(IBlob, )
supermod.IBlobs.subclass = IBlobsSub
# end class IBlobsSub


class proxySub(supermod.proxy):
    def __init__(self, id=None, locator=None, type_=None, objectId=None, annotations=None):
        super(proxySub, self).__init__(id, locator, type_, objectId, annotations, )
supermod.proxy.subclass = proxySub
# end class proxySub


class proxiesSub(supermod.proxies):
    def __init__(self, proxy=None):
        super(proxiesSub, self).__init__(proxy, )
supermod.proxies.subclass = proxiesSub
# end class proxiesSub


class IGenericAnnotationsSub(supermod.IGenericAnnotations):
    def __init__(self, anytypeobjs_=None):
        super(IGenericAnnotationsSub, self).__init__(anytypeobjs_, )
supermod.IGenericAnnotations.subclass = IGenericAnnotationsSub
# end class IGenericAnnotationsSub


class crcSub(supermod.crc):
    def __init__(self, value=None):
        super(crcSub, self).__init__(value, )
supermod.crc.subclass = crcSub
# end class crcSub


class IMXSub(supermod.IMX):
    def __init__(self):
        super(IMXSub, self).__init__()
supermod.IMX.subclass = IMXSub
# end class IMXSub


class CommandSub(supermod.Command):
    def __init__(self, id=None, idref=None, iid=None, command=None, commandTimeout=None, annotations=None):
        super(CommandSub, self).__init__(id, idref, iid, command, commandTimeout, annotations, )
supermod.Command.subclass = CommandSub
# end class CommandSub


class ComputeNodeConfigurationSub(supermod.ComputeNodeConfiguration):
    def __init__(self, id=None, idref=None, iid=None, nodeName=None, annotations=None, options=None):
        super(ComputeNodeConfigurationSub, self).__init__(id, idref, iid, nodeName, annotations, options, )
supermod.ComputeNodeConfiguration.subclass = ComputeNodeConfigurationSub
# end class ComputeNodeConfigurationSub


class DomainObjectLocateSub(supermod.DomainObjectLocate):
    def __init__(self, id=None, idref=None, iid=None, objName=None, objType=None, permission=None, serviceType=None, annotations=None, folderObjects=None):
        super(DomainObjectLocateSub, self).__init__(id, idref, iid, objName, objType, permission, serviceType, annotations, folderObjects, )
supermod.DomainObjectLocate.subclass = DomainObjectLocateSub
# end class DomainObjectLocateSub


class RoleTypeContainerSub(supermod.RoleTypeContainer):
    def __init__(self, id=None, idref=None, iid=None, roleType=None, annotations=None):
        super(RoleTypeContainerSub, self).__init__(id, idref, iid, roleType, annotations, )
supermod.RoleTypeContainer.subclass = RoleTypeContainerSub
# end class RoleTypeContainerSub


class NodeCapabilitySub(supermod.NodeCapability):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, type_=None, resources=None):
        super(NodeCapabilitySub, self).__init__(id, idref, iid, annotations, type_, resources, )
supermod.NodeCapability.subclass = NodeCapabilitySub
# end class NodeCapabilitySub


class ProcessSub(supermod.Process):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, jvmOptions=None, node=None, primaryProcess=None, envVariables=None, internalProcessOptions=None, postStartCommand=None, preStartCommand=None, processOptions=None):
        super(ProcessSub, self).__init__(id, idref, iid, annotations, jvmOptions, node, primaryProcess, envVariables, internalProcessOptions, postStartCommand, preStartCommand, processOptions, )
supermod.Process.subclass = ProcessSub
# end class ProcessSub


class ServiceRefSub(supermod.ServiceRef):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, domainName=None, serviceName=None, serviceRefType=None, options=None):
        super(ServiceRefSub, self).__init__(id, idref, iid, annotations, domainName, serviceName, serviceRefType, options, )
supermod.ServiceRef.subclass = ServiceRefSub
# end class ServiceRefSub


class CppProcessSub(supermod.CppProcess):
    def __init__(self):
        super(CppProcessSub, self).__init__()
supermod.CppProcess.subclass = CppProcessSub
# end class CppProcessSub


class DomainObjSub(supermod.DomainObj):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, name=None, description=None, extensiontype_=None):
        super(DomainObjSub, self).__init__(id, idref, iid, annotations, name, description, extensiontype_, )
supermod.DomainObj.subclass = DomainObjSub
# end class DomainObjSub


class EarlierVersionDomainObjRefsSub(supermod.EarlierVersionDomainObjRefs):
    def __init__(self, objIds=None):
        super(EarlierVersionDomainObjRefsSub, self).__init__(objIds, )
supermod.EarlierVersionDomainObjRefs.subclass = EarlierVersionDomainObjRefsSub
# end class EarlierVersionDomainObjRefsSub


class ExecutableProcessSub(supermod.ExecutableProcess):
    def __init__(self, base64Encode=None, commandArguments=None, commandName=None):
        super(ExecutableProcessSub, self).__init__(base64Encode, commandArguments, commandName, )
supermod.ExecutableProcess.subclass = ExecutableProcessSub
# end class ExecutableProcessSub


class JSFProcessSub(supermod.JSFProcess):
    def __init__(self):
        super(JSFProcessSub, self).__init__()
supermod.JSFProcess.subclass = JSFProcessSub
# end class JSFProcessSub


class NodeResourceSub(supermod.NodeResource):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, name=None, available=None, type_=None):
        super(NodeResourceSub, self).__init__(id, idref, iid, annotations, name, available, type_, )
supermod.NodeResource.subclass = NodeResourceSub
# end class NodeResourceSub


class ResourceStringSub(supermod.ResourceString):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, name=None, available=None):
        super(ResourceStringSub, self).__init__(id, idref, iid, annotations, name, available, )
supermod.ResourceString.subclass = ResourceStringSub
# end class ResourceStringSub


class WebAppProcessSub(supermod.WebAppProcess):
    def __init__(self, algorithm=None, httpPort=None, httpsPort=None, keystoreFile=None, keystorePassword=None, maxQueue=None, maxRequests=None, shutdownPort=None, sslProtocol=None, truststoreFile=None, truststorePassword=None):
        super(WebAppProcessSub, self).__init__(algorithm, httpPort, httpsPort, keystoreFile, keystorePassword, maxQueue, maxRequests, shutdownPort, sslProtocol, truststoreFile, truststorePassword, )
supermod.WebAppProcess.subclass = WebAppProcessSub
# end class WebAppProcessSub


class FolderSub(supermod.Folder):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, name=None, description=None):
        super(FolderSub, self).__init__(id, idref, iid, annotations, name, description, )
supermod.Folder.subclass = FolderSub
# end class FolderSub


class GridSub(supermod.Grid):
    def __init__(self, nodes=None):
        super(GridSub, self).__init__(nodes, )
supermod.Grid.subclass = GridSub
# end class GridSub


class InstalledNodeResourceSub(supermod.InstalledNodeResource):
    def __init__(self, vendorId=None, vendorName=None, version=None):
        super(InstalledNodeResourceSub, self).__init__(vendorId, vendorName, version, )
supermod.InstalledNodeResource.subclass = InstalledNodeResourceSub
# end class InstalledNodeResourceSub


class NodeSub(supermod.Node):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, name=None, description=None, nodeOptions=None):
        super(NodeSub, self).__init__(id, idref, iid, annotations, name, description, nodeOptions, )
supermod.Node.subclass = NodeSub
# end class NodeSub


class ResourceStringWithValueSub(supermod.ResourceStringWithValue):
    def __init__(self, value=None):
        super(ResourceStringWithValueSub, self).__init__(value, )
supermod.ResourceStringWithValue.subclass = ResourceStringWithValueSub
# end class ResourceStringWithValueSub


class ServiceSub(supermod.Service):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, name=None, description=None):
        super(ServiceSub, self).__init__(id, idref, iid, annotations, name, description, )
supermod.Service.subclass = ServiceSub
# end class ServiceSub


class ApplicationServiceSub(supermod.ApplicationService):
    def __init__(self, gridName=None, licenseName=None, serviceType=None, serviceVersion=None, computeNodeConfigurations=None, defaultComputeNodeOptions=None, internalServiceOptions=None, serviceOptions=None, serviceProcesses=None, serviceRefs=None):
        super(ApplicationServiceSub, self).__init__(gridName, licenseName, serviceType, serviceVersion, computeNodeConfigurations, defaultComputeNodeOptions, internalServiceOptions, serviceOptions, serviceProcesses, serviceRefs, )
supermod.ApplicationService.subclass = ApplicationServiceSub
# end class ApplicationServiceSub


class CoreServiceSub(supermod.CoreService):
    def __init__(self):
        super(CoreServiceSub, self).__init__()
supermod.CoreService.subclass = CoreServiceSub
# end class CoreServiceSub


class DomainNodeSub(supermod.DomainNode):
    def __init__(self, associated=None, portal=None, address=None, capabilities=None, options=None, predefineResources=None, resource=None, roles=None, user=None):
        super(DomainNodeSub, self).__init__(associated, portal, address, capabilities, options, predefineResources, resource, roles, user, )
supermod.DomainNode.subclass = DomainNodeSub
# end class DomainNodeSub


class RemoteNodeSub(supermod.RemoteNode):
    def __init__(self):
        super(RemoteNodeSub, self).__init__()
supermod.RemoteNode.subclass = RemoteNodeSub
# end class RemoteNodeSub


class linkedDomainsTypeSub(supermod.linkedDomainsType):
    def __init__(self, LinkedDomain=None):
        super(linkedDomainsTypeSub, self).__init__(LinkedDomain, )
supermod.linkedDomainsType.subclass = linkedDomainsTypeSub
# end class linkedDomainsTypeSub


class portalsTypeSub(supermod.portalsType):
    def __init__(self, NodeRef=None):
        super(portalsTypeSub, self).__init__(NodeRef, )
supermod.portalsType.subclass = portalsTypeSub
# end class portalsTypeSub


class predefinedResourcesTypeSub(supermod.predefinedResourcesType):
    def __init__(self, NodeResource=None):
        super(predefinedResourcesTypeSub, self).__init__(NodeResource, )
supermod.predefinedResourcesType.subclass = predefinedResourcesTypeSub
# end class predefinedResourcesTypeSub


class resourcesTypeSub(supermod.resourcesType):
    def __init__(self, NodeResource=None):
        super(resourcesTypeSub, self).__init__(NodeResource, )
supermod.resourcesType.subclass = resourcesTypeSub
# end class resourcesTypeSub


class processStatesTypeSub(supermod.processStatesType):
    def __init__(self, ServiceProcessStartupState=None):
        super(processStatesTypeSub, self).__init__(ServiceProcessStartupState, )
supermod.processStatesType.subclass = processStatesTypeSub
# end class processStatesTypeSub


class serviceStatesTypeSub(supermod.serviceStatesType):
    def __init__(self, ServiceStartupState=None):
        super(serviceStatesTypeSub, self).__init__(ServiceStartupState, )
supermod.serviceStatesType.subclass = serviceStatesTypeSub
# end class serviceStatesTypeSub


class domainOptionsTypeSub(supermod.domainOptionsType):
    def __init__(self, OptionGroup=None):
        super(domainOptionsTypeSub, self).__init__(OptionGroup, )
supermod.domainOptionsType.subclass = domainOptionsTypeSub
# end class domainOptionsTypeSub


class configSettingsTypeSub(supermod.configSettingsType):
    def __init__(self, OptionGroup=None):
        super(configSettingsTypeSub, self).__init__(OptionGroup, )
supermod.configSettingsType.subclass = configSettingsTypeSub
# end class configSettingsTypeSub


class gatewaysTypeSub(supermod.gatewaysType):
    def __init__(self, NodeAddress=None):
        super(gatewaysTypeSub, self).__init__(NodeAddress, )
supermod.gatewaysType.subclass = gatewaysTypeSub
# end class gatewaysTypeSub


class optionsTypeSub(supermod.optionsType):
    def __init__(self, Option=None):
        super(optionsTypeSub, self).__init__(Option, )
supermod.optionsType.subclass = optionsTypeSub
# end class optionsTypeSub


class optionsType1Sub(supermod.optionsType1):
    def __init__(self, OptionGroup=None):
        super(optionsType1Sub, self).__init__(OptionGroup, )
supermod.optionsType1.subclass = optionsType1Sub
# end class optionsType1Sub


class folderObjectsTypeSub(supermod.folderObjectsType):
    def __init__(self, DomainObjectLocate=None):
        super(folderObjectsTypeSub, self).__init__(DomainObjectLocate, )
supermod.folderObjectsType.subclass = folderObjectsTypeSub
# end class folderObjectsTypeSub


class resourcesType2Sub(supermod.resourcesType2):
    def __init__(self, ResourceString=None):
        super(resourcesType2Sub, self).__init__(ResourceString, )
supermod.resourcesType2.subclass = resourcesType2Sub
# end class resourcesType2Sub


class envVariablesTypeSub(supermod.envVariablesType):
    def __init__(self, Option=None):
        super(envVariablesTypeSub, self).__init__(Option, )
supermod.envVariablesType.subclass = envVariablesTypeSub
# end class envVariablesTypeSub


class internalProcessOptionsTypeSub(supermod.internalProcessOptionsType):
    def __init__(self, OptionGroup=None):
        super(internalProcessOptionsTypeSub, self).__init__(OptionGroup, )
supermod.internalProcessOptionsType.subclass = internalProcessOptionsTypeSub
# end class internalProcessOptionsTypeSub


class processOptionsTypeSub(supermod.processOptionsType):
    def __init__(self, OptionGroup=None):
        super(processOptionsTypeSub, self).__init__(OptionGroup, )
supermod.processOptionsType.subclass = processOptionsTypeSub
# end class processOptionsTypeSub


class optionsType3Sub(supermod.optionsType3):
    def __init__(self, OptionGroup=None):
        super(optionsType3Sub, self).__init__(OptionGroup, )
supermod.optionsType3.subclass = optionsType3Sub
# end class optionsType3Sub


class nodeOptionsTypeSub(supermod.nodeOptionsType):
    def __init__(self, OptionGroup=None):
        super(nodeOptionsTypeSub, self).__init__(OptionGroup, )
supermod.nodeOptionsType.subclass = nodeOptionsTypeSub
# end class nodeOptionsTypeSub


class computeNodeConfigurationsTypeSub(supermod.computeNodeConfigurationsType):
    def __init__(self, ComputeNodeConfiguration=None):
        super(computeNodeConfigurationsTypeSub, self).__init__(ComputeNodeConfiguration, )
supermod.computeNodeConfigurationsType.subclass = computeNodeConfigurationsTypeSub
# end class computeNodeConfigurationsTypeSub


class defaultComputeNodeOptionsTypeSub(supermod.defaultComputeNodeOptionsType):
    def __init__(self, OptionGroup=None):
        super(defaultComputeNodeOptionsTypeSub, self).__init__(OptionGroup, )
supermod.defaultComputeNodeOptionsType.subclass = defaultComputeNodeOptionsTypeSub
# end class defaultComputeNodeOptionsTypeSub


class internalServiceOptionsTypeSub(supermod.internalServiceOptionsType):
    def __init__(self, OptionGroup=None):
        super(internalServiceOptionsTypeSub, self).__init__(OptionGroup, )
supermod.internalServiceOptionsType.subclass = internalServiceOptionsTypeSub
# end class internalServiceOptionsTypeSub


class serviceOptionsTypeSub(supermod.serviceOptionsType):
    def __init__(self, OptionGroup=None):
        super(serviceOptionsTypeSub, self).__init__(OptionGroup, )
supermod.serviceOptionsType.subclass = serviceOptionsTypeSub
# end class serviceOptionsTypeSub


class serviceProcessesTypeSub(supermod.serviceProcessesType):
    def __init__(self, Process=None):
        super(serviceProcessesTypeSub, self).__init__(Process, )
supermod.serviceProcessesType.subclass = serviceProcessesTypeSub
# end class serviceProcessesTypeSub


class serviceRefsTypeSub(supermod.serviceRefsType):
    def __init__(self, ServiceRef=None):
        super(serviceRefsTypeSub, self).__init__(ServiceRef, )
supermod.serviceRefsType.subclass = serviceRefsTypeSub
# end class serviceRefsTypeSub


class capabilitiesTypeSub(supermod.capabilitiesType):
    def __init__(self, NodeCapability=None):
        super(capabilitiesTypeSub, self).__init__(NodeCapability, )
supermod.capabilitiesType.subclass = capabilitiesTypeSub
# end class capabilitiesTypeSub


class optionsType4Sub(supermod.optionsType4):
    def __init__(self, OptionGroup=None):
        super(optionsType4Sub, self).__init__(OptionGroup, )
supermod.optionsType4.subclass = optionsType4Sub
# end class optionsType4Sub


class predefineResourcesTypeSub(supermod.predefineResourcesType):
    def __init__(self, NodeResource=None):
        super(predefineResourcesTypeSub, self).__init__(NodeResource, )
supermod.predefineResourcesType.subclass = predefineResourcesTypeSub
# end class predefineResourcesTypeSub


class resourceTypeSub(supermod.resourceType):
    def __init__(self, NodeResource=None):
        super(resourceTypeSub, self).__init__(NodeResource, )
supermod.resourceType.subclass = resourceTypeSub
# end class resourceTypeSub


class rolesTypeSub(supermod.rolesType):
    def __init__(self, RoleTypeContainer=None):
        super(rolesTypeSub, self).__init__(RoleTypeContainer, )
supermod.rolesType.subclass = rolesTypeSub
# end class rolesTypeSub


class LinkedDomainSub(supermod.LinkedDomain):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, name=None, description=None, gateways=None):
        super(LinkedDomainSub, self).__init__(id, idref, iid, annotations, name, description, gateways, )
supermod.LinkedDomain.subclass = LinkedDomainSub
# end class LinkedDomainSub


class DomainServiceConfigSub(supermod.DomainServiceConfig):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, name=None, builtinServiceFolderName=None, domainDescription=None, domainOptions=None):
        super(DomainServiceConfigSub, self).__init__(id, idref, iid, annotations, name, builtinServiceFolderName, domainDescription, domainOptions, )
supermod.DomainServiceConfig.subclass = DomainServiceConfigSub
# end class DomainServiceConfigSub


class StoredStartupStateSub(supermod.StoredStartupState):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, name=None, processStates=None, serviceStates=None):
        super(StoredStartupStateSub, self).__init__(id, idref, iid, annotations, name, processStates, serviceStates, )
supermod.StoredStartupState.subclass = StoredStartupStateSub
# end class StoredStartupStateSub


class ServiceRuntimeSub(supermod.ServiceRuntime):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, state=None, service=None):
        super(ServiceRuntimeSub, self).__init__(id, idref, iid, annotations, state, service, )
supermod.ServiceRuntime.subclass = ServiceRuntimeSub
# end class ServiceRuntimeSub


class ProcessRuntimeSub(supermod.ProcessRuntime):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, nodeName=None, pid=None, port=None, primary=None, serviceName=None, serviceURL=None, state=None):
        super(ProcessRuntimeSub, self).__init__(id, idref, iid, annotations, nodeName, pid, port, primary, serviceName, serviceURL, state, )
supermod.ProcessRuntime.subclass = ProcessRuntimeSub
# end class ProcessRuntimeSub


class NodeConfigSub(supermod.NodeConfig):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, adminconsolePort=None, adminconsoleShutdownPort=None, domainName=None, logServiceDir=None, nodeName=None, options=None, resetHostPort=None, systemLogDir=None, tlsEnabled=None, address=None, earlierInfaHomeConfig=None, httpsInfo=None, portals=None, predefinedResources=None, resources=None, securityConfig=None, extensiontype_=None):
        super(NodeConfigSub, self).__init__(id, idref, iid, annotations, adminconsolePort, adminconsoleShutdownPort, domainName, logServiceDir, nodeName, options, resetHostPort, systemLogDir, tlsEnabled, address, earlierInfaHomeConfig, httpsInfo, portals, predefinedResources, resources, securityConfig, extensiontype_, )
supermod.NodeConfig.subclass = NodeConfigSub
# end class NodeConfigSub


class LinkedDomainStorageSub(supermod.LinkedDomainStorage):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, name=None, linkedDomains=None):
        super(LinkedDomainStorageSub, self).__init__(id, idref, iid, annotations, name, linkedDomains, )
supermod.LinkedDomainStorage.subclass = LinkedDomainStorageSub
# end class LinkedDomainStorageSub


class WorkerNodeConfigSub(supermod.WorkerNodeConfig):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, adminconsolePort=None, adminconsoleShutdownPort=None, domainName=None, logServiceDir=None, nodeName=None, options=None, resetHostPort=None, systemLogDir=None, tlsEnabled=None, address=None, earlierInfaHomeConfig=None, httpsInfo=None, portals=None, predefinedResources=None, resources=None, securityConfig=None, encryptedPassword=None, securityDomain=None, username=None):
        super(WorkerNodeConfigSub, self).__init__(id, idref, iid, annotations, adminconsolePort, adminconsoleShutdownPort, domainName, logServiceDir, nodeName, options, resetHostPort, systemLogDir, tlsEnabled, address, earlierInfaHomeConfig, httpsInfo, portals, predefinedResources, resources, securityConfig, encryptedPassword, securityDomain, username, )
supermod.WorkerNodeConfig.subclass = WorkerNodeConfigSub
# end class WorkerNodeConfigSub


class GatewayNodeConfigSub(supermod.GatewayNodeConfig):
    def __init__(self, id=None, idref=None, iid=None, annotations=None, adminconsolePort=None, adminconsoleShutdownPort=None, domainName=None, logServiceDir=None, nodeName=None, options=None, resetHostPort=None, systemLogDir=None, tlsEnabled=None, address=None, earlierInfaHomeConfig=None, httpsInfo=None, portals=None, predefinedResources=None, resources=None, securityConfig=None, dbConnectivity=None, configSettings=None):
        super(GatewayNodeConfigSub, self).__init__(id, idref, iid, annotations, adminconsolePort, adminconsoleShutdownPort, domainName, logServiceDir, nodeName, options, resetHostPort, systemLogDir, tlsEnabled, address, earlierInfaHomeConfig, httpsInfo, portals, predefinedResources, resources, securityConfig, dbConnectivity, configSettings, )
supermod.GatewayNodeConfig.subclass = GatewayNodeConfigSub
# end class GatewayNodeConfigSub


def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    rootClass = supermod.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DBConnectivity'
        rootClass = supermod.DBConnectivity
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:domainservice="http://com.informatica.isp.metadata.domainservice/2"',
            pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DBConnectivity'
        rootClass = supermod.DBConnectivity
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(content)
        sys.stdout.write('\n')
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False):
    if sys.version_info.major == 2:
        from StringIO import StringIO
    else:
        from io import BytesIO as StringIO
    parser = None
    doc = parsexml_(StringIO(inString), parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DBConnectivity'
        rootClass = supermod.DBConnectivity
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:domainservice="http://com.informatica.isp.metadata.domainservice/2"')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DBConnectivity'
        rootClass = supermod.DBConnectivity
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('#from domainservice import *\n\n')
        sys.stdout.write('import domainservice as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()
