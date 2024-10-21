##########################################################################
# OpenWebif: BQEController
##########################################################################
# Copyright (C) 2013 - 2022 jbleyel and E2OpenPlugins
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
##########################################################################
from os import remove
import json
from twisted.web import static, resource, http
from enigma import eServiceCenter, eServiceReference
from Components.config import config
from Components.ParentalControl import parentalControl
from .utilities import getUrlArg, toBinary, toString, e2simplexmlresult
from .defaults import service_types_tv, LCNSUPPORT
from .models.services import getPicon
from .BouquetEditor import BouquetEditor
from .base import BaseController
from .i18n import _


class BQEWebController(BaseController):
	def __init__(self, session, path=""):
		BaseController.__init__(self, path=path, session=session)

	def returnResult(self, req, result):
		if self.isJson:
			return {"Result": result}
		else:
			state = result[0]
			statetext = result[1]
			req.setResponseCode(http.OK)
			req.setHeader('Content-type', 'application/xhtml+xml')
			req.setHeader('charset', 'UTF-8')
			return e2simplexmlresult(state, statetext)

	def buildCommand(self, ids, args):
		paramlist = ids.split(",")
		cmddata = {}
		for key in paramlist:
			k = toBinary(key)
			if k in args:
				cmddata[key] = toString(args[k][0])
			else:
				cmddata[key] = None
		return cmddata

	def prePageLoad(self, request):
		request.setHeader("content-type", "text/xml")

	def P_addbouquet(self, request):
		self.withMainTemplate = False
		bqe = BouquetEditor(self.session, func=BouquetEditor.ADD_BOUQUET)
		bqe.handleCommand(self.buildCommand('name,mode', request.args))
		return self.returnResult(request, bqe.result)

	def P_removebouquet(self, request):
		self.withMainTemplate = False
		bqe = BouquetEditor(self.session, func=BouquetEditor.REMOVE_BOUQUET)
		bqe.handleCommand(self.buildCommand('sBouquetRef,mode', request.args))
		return self.returnResult(request, bqe.result)

	def P_movebouquet(self, request):
		self.withMainTemplate = False
		bqe = BouquetEditor(self.session, func=BouquetEditor.MOVE_BOUQUET)
		bqe.handleCommand(self.buildCommand('sBouquetRef,mode,position', request.args))
		return self.returnResult(request, bqe.result)

	def P_addmarkertobouquet(self, request):
		self.withMainTemplate = False
		bqe = BouquetEditor(self.session, func=BouquetEditor.ADD_MARKER_TO_BOUQUET)
		bqe.handleCommand(self.buildCommand('sBouquetRef,Name,sRefBefore,SP', request.args))
		return self.returnResult(request, bqe.result)

	def P_addservicetobouquet(self, request):
		self.withMainTemplate = False
		bqe = BouquetEditor(self.session, func=BouquetEditor.ADD_SERVICE_TO_BOUQUET)
		bqe.handleCommand(self.buildCommand('sBouquetRef,sRef,sRefBefore,sRefUrl,Name,SubName', request.args))
		return self.returnResult(request, bqe.result)

	def P_addprovidertobouquetlist(self, request):
		self.withMainTemplate = False
		bqe = BouquetEditor(self.session, func=BouquetEditor.ADD_PROVIDER_TO_BOUQUETLIST)
		bqe.handleCommand(self.buildCommand('sProviderRef,mode', request.args))
		return self.returnResult(request, bqe.result)

	def P_addservicetoalternative(self, request):
		self.withMainTemplate = False
		bqe = BouquetEditor(self.session, func=BouquetEditor.ADD_SERVICE_TO_ALTERNATIVE)
		bqe.handleCommand(self.buildCommand('sBouquetRef,sCurrentRef,sRef,mode', request.args))
		return self.returnResult(request, bqe.result)

	def P_moveservice(self, request):
		self.withMainTemplate = False
		bqe = BouquetEditor(self.session, func=BouquetEditor.MOVE_SERVICE)
		bqe.handleCommand(self.buildCommand('sBouquetRef,sRef,mode,position', request.args))
		return self.returnResult(request, bqe.result)

	def P_removeservice(self, request):
		self.withMainTemplate = False
		bqe = BouquetEditor(self.session, func=BouquetEditor.REMOVE_SERVICE)
		bqe.handleCommand(self.buildCommand('sBouquetRef,sRef', request.args))
		return self.returnResult(request, bqe.result)

	def P_renameservice(self, request):
		self.withMainTemplate = False
		bqe = BouquetEditor(self.session, func=BouquetEditor.RENAME_SERVICE)
		bqe.handleCommand(self.buildCommand('sBouquetRef,sRef,sRefBefore,newName,mode', request.args))
		return self.returnResult(request, bqe.result)

	def P_removealternativeservices(self, request):
		self.withMainTemplate = False
		bqe = BouquetEditor(self.session, func=BouquetEditor.REMOVE_ALTERNATIVE_SERVICES)
		bqe.handleCommand(self.buildCommand('sBouquetRef,sRef', request.args))
		return self.returnResult(request, bqe.result)

	def P_togglelock(self, request):
		self.withMainTemplate = False
		bqe = BouquetEditor(self.session, func=BouquetEditor.TOGGLE_LOCK)
		bqe.handleCommand(self.buildCommand('sRef,password', request.args))
		return self.returnResult(request, bqe.result)

	def P_backup(self, request):
		self.withMainTemplate = False
		bqe = BouquetEditor(self.session, func=BouquetEditor.BACKUP)
		bqe.handleCommand(toString(request.args[b'Filename'][0]))
		return self.returnResult(request, bqe.result)

	def P_restore(self, request):
		self.withMainTemplate = False
		bqe = BouquetEditor(self.session, func=BouquetEditor.RESTORE)
		bqe.handleCommand(toString(request.args[b'Filename'][0]))
		return self.returnResult(request, bqe.result)

#	def P_calcpos(self, request):
#		type = 0
#		if "type" in request.args.keys():
#			type = request.args["type"][0]
#		bRef = '%s FROM BOUQUET "bouquets.tv" ORDER BY bouquet' % (service_types_tv)
#		if type == 1:
#			bRef = '%s FROM BOUQUET "bouquets.radio" ORDER BY bouquet' % (service_types_radio)
#
#		servicehandler = eServiceCenter.getInstance()
#		serviceslist = servicehandler.list(eServiceReference(bRef))
#		bqlist = serviceslist and serviceslist.getContent("RN", True)
#		pos = 0
#		services = []
#		for bq in bqlist:
#			bqref = bq[0].toString()
#			service = {}
#			service['servicereference'] = bqref
#			service['startpos'] = pos
#			serviceslist = servicehandler.list(eServiceReference(bqref))
#			fulllist = serviceslist and serviceslist.getContent("RN", True)
#			for item in fulllist:
#				sref = item[0].toString()
#				hs = (int(sref.split(":")[1]) & 512)
#				sp = (sref[:7] == '1:832:D')
#				if not hs or sp:  # 512 is hidden service on sifteam image. Doesn't affect other images
#					pos = pos + 1
#					if not sp and item[0].flags & eServiceReference.isMarker:
#						pos = pos - 1
#			services.append(service)
#		return {"services": services}

	def P_getservices(self, request):
		sref = getUrlArg(request, "sRef", "")
		includepicon = (getUrlArg(request, "picon", "") == '1')
		services = []

		lcn = LCNSUPPORT and config.usage.numberMode.value == 2
		calcpos = False

		if sref == "":
			sref = f'{service_types_tv} FROM BOUQUET "bouquets.tv" ORDER BY bouquet'
			calcpos = True
			lcn = False
		elif ' "bouquets.radio" ' in sref:
			calcpos = True
		elif ' "bouquets.tv" ' in sref:
			calcpos = True

		if lcn:
			calcpos = False

		servicehandler = eServiceCenter.getInstance()
		serviceslist = servicehandler.list(eServiceReference(sref))
		fulllist = serviceslist and serviceslist.getContent("RNL" if lcn else "RN", True)

		pos = 0
		opos = 0
		for item in fulllist:
			oldopos = opos
			if calcpos:
				sref = item[0].toString()
				serviceslist = servicehandler.list(eServiceReference(sref))
				sfulllist = serviceslist and serviceslist.getContent("RN", True)
				for sitem in sfulllist:
					sref = sitem[0].toString()
					hs = (int(sref.split(":")[1]) & 512)
					sp = sitem[0].flags & eServiceReference.isNumberedMarker
					if not hs or sp:  # 512 is hidden service on sifteam image. Doesn't affect other images
						opos = opos + 1
						if not sp and sitem[0].flags & eServiceReference.isMarker:
							opos = opos - 1
			sref = item[0].toString()
			hs = (int(sref.split(":")[1]) & 512)
			sp = item[0].flags & eServiceReference.isNumberedMarker
			if not hs or sp:  # 512 is hidden service on sifteam image. Doesn't affect other images
				pos = pos + 1
				service = {}
				if calcpos:
					service['startpos'] = oldopos
				service['pos'] = item[2] if lcn else pos
				service['servicereference'] = sref
				service['isgroup'] = '0'
				service['ismarker'] = '0'
				service['isprotected'] = '0'
				if includepicon:
					try:
						service['picon'] = getPicon(sref)
					except:  # nosec # noqa: E722
						service['picon'] = ''
				if sp:
					service['ismarker'] = '2'
					service['servicename'] = ''
				else:
					service['servicename'] = item[1].replace('<', '&lt;').replace('>', '&gt;')
					if item[0].flags & eServiceReference.isGroup:
						gservices = []
						service['isgroup'] = '1'
						# get members of group
						gserviceslist = servicehandler.list(eServiceReference(sref))
						gfulllist = gserviceslist and gserviceslist.getContent("RN", True)
						for gitem in gfulllist:
							gservice = {}
							gservice['servicereference'] = gitem[0].toString()
							gservice['servicename'] = gitem[1].replace('<', '&lt;').replace('>', '&gt;')
							gservices.append(gservice)
						service['members'] = gservices

					if item[0].flags & eServiceReference.isMarker:
						service['ismarker'] = '1'
						# dont inc the pos for markers
						pos = pos - 1
						service['pos'] = 0
				if not sp and config.ParentalControl.configured.value and config.ParentalControl.servicepinactive.value:
					sref = item[0].toCompareString()
					protection = parentalControl.getProtectionLevel(sref)
					if protection != -1:
						if config.ParentalControl.type.value == "blacklist":
							if sref in parentalControl.blacklist:
								if "SERVICE" in parentalControl.blacklist[sref]:
									service['isprotected'] = '1'
								elif "BOUQUET" in parentalControl.blacklist[sref]:
									service['isprotected'] = '2'
								else:
									service['isprotected'] = '3'
						elif config.ParentalControl.type.value == "whitelist":
							if sref not in parentalControl.whitelist:
								if item[0].flags & eServiceReference.isGroup:
									service['isprotected'] = '5'
								else:
									service['isprotected'] = '4'
				services.append(service)
		return {"services": services}

	def P_getprotectionsettings(self, request):
		configured = config.ParentalControl.configured.value
		if configured:
			if config.ParentalControl.type.value == "blacklist":
				protectiontype = "0"
			else:
				protectiontype = "1"
			setuppin = "setuppin" in list(config.ParentalControl.dict().keys()) and config.ParentalControl.setuppin.value or -1
			setuppinactive = "setuppin" in list(config.ParentalControl.dict().keys()) and config.ParentalControl.setuppinactive.value
		else:
			protectiontype = ""
			setuppin = ""
			setuppinactive = ""

		ps = {}
		ps['Configured'] = configured
		ps['Type'] = protectiontype
		ps['SetupPinActive'] = setuppinactive
		ps['SetupPin'] = setuppin
		return {"ps": ps}


class BQEUploadFile(resource.Resource):
	FN = "/tmp/bouquets_backup.tar"  # nosec

	def __init__(self, session):
		self.session = session
		resource.Resource.__init__(self)

	def render_POST(self, request):
		request.setResponseCode(http.OK)
		request.setHeader('content-type', 'text/plain')
		request.setHeader('charset', 'UTF-8')
		content = request.args[b'rfile'][0]
		if not content:
			result = [False, 'Error upload File']
		else:
			with open(self.FN, "wb") as fd:
				bytecount = fd.write(content)
			if bytecount <= 0:
				try:
					remove(self.FN)
				except OSError:
					pass
				result = [False, _("Error writing File")]
			else:
				result = [True, self.FN]
		return json.dumps({"Result": result}).encode("UTF-8")


class BQEImport(resource.Resource):
	def __init__(self, session):
		self.session = session
		resource.Resource.__init__(self)

	def render_POST(self, request):
		request.setResponseCode(http.OK)
		request.setHeader('content-type', 'text/plain')
		request.setHeader('charset', 'UTF-8')
		result = [False, 'Error upload File']
		if getUrlArg(request, "json") is not None:
			bqe = BouquetEditor(self.session, func=BouquetEditor.IMPORT_BOUQUET)
			bqe.handleCommand(request.args)
			result = bqe.result

		return json.dumps({"Result": result}).encode("UTF-8")


class BQEApiController(BQEWebController):
	def __init__(self, session, path=""):
		BQEWebController.__init__(self, session, path)

	def prePageLoad(self, request):
		self.isJson = True


class BQEController(BaseController):
	def __init__(self, session, path=""):
		BaseController.__init__(self, path=path, session=session)
		self.putChild(b"web", BQEWebController(session))
		self.putChild(b"api", BQEApiController(session))
		self.putChild(b"tmp", static.File(b"/tmp"))  # nosec
		self.putChild(b"uploadrestore", BQEUploadFile(session))
		self.putChild(b"import", BQEImport(session))
