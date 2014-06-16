# coding=utf-8
from django import forms
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

from  patmgr.models import Patent
from rankmgr.models import PatentPackage, PatentRatingReport, PatentExpertRating

class PatentPackageCreateForm(forms.ModelForm):
	selected_patent_list = forms.CharField(max_length=4096, label='专利列表', widget=forms.HiddenInput())
	class Meta:
		model = PatentPackage
		fields = [ 'name' ]
		widgets = {
			'name': forms.TextInput(attrs={'class':'text-input large-input'}),
		}

	def save(self, commit=True):
		instance = super(PatentPackageCreateForm, self).save(commit)
		for patent_id in self.cleaned_data["selected_patent_list"].split('&'):
			if not patent_id: continue
			try:
				report = PatentRatingReport(package = instance,
											patent = Patent.objects.get(pk=patent_id))
				report.save();
				print u"SUCCESS create report for: %s\n" % report.__unicode__()
			except:
				#print u"ERR create report for: %s, %s\n" % (instance.__unicode__(), patent_id)
				continue
		return instance

class PatentExpertRatingForm(forms.ModelForm):
	action = forms.CharField(widget=forms.HiddenInput(), initial="save")
	class Meta:
		model = PatentExpertRating
		fields = [ 'rank', 'remark', 'submit_date' ]
		RATING_CHOICES = ((1,1), (2,2), (3,3), (4,4), (5,5),)
		widgets = {
			'rank': forms.RadioSelect(attrs={'class':'star'}, choices=RATING_CHOICES),
			'remark': forms.Textarea(attrs={'class':'text-input large-input'}),
		}
	def save(self, commit=True):
		if self.cleaned_data["action"] == "submit":
			self.instance.submit_date = datetime.now()
		else:
			self.instance.submit_date = None
		instance = super(PatentExpertRatingForm, self).save(commit)
		return instance

