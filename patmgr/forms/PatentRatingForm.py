# coding=utf-8
from django import forms
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from patmgr.models import Patent
from patmgr.models import PatentPackage, PatentRatingReport

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

