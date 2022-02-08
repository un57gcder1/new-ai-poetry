from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpRequest
from .generator import generate_rhyme_abab_poetry, generate_rhyme_aabb_poetry, generate_rhyme_a_poetry, generate_rhyme_aaa_poetry
# Create your views here.

class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        
        """min_char = self.request.GET.get('min_char')
        max_char = self.request.GET.get('max_char')"""
        state_size = self.request.GET.get('creativity')
        lines = self.request.GET.get('lines')
        rhyme_scheme = self.request.GET.get('rhyme_scheme')
        
        if state_size == None or lines == None or rhyme_scheme == None: # Removed """max_char == None or""" """min_char == None or""" for later implementation
            return context
        
        else:
           if self.validation(state_size, lines, rhyme_scheme) == False: # Removed """min_char, max_char, """ for later implementation
               context['error'] = "Please use the form. " # Insert title here
               return context
            
           context['state_size'] = self.request.GET.get('creativity')
           """context['min_char'] = self.request.GET.get('min_char')
           context['max_char'] = self.request.GET.get('max_char')"""
           context['lines'] = self.request.GET.get('lines')

           """ min_char = int(self.request.GET.get('min_char'))
           max_char = int(self.request.GET.get('max_char'))"""
           state_size = int(self.request.GET.get('creativity'))
           lines = int(self.request.GET.get('lines'))
           
           """if min_char >= max_char:
               context['error'] = "Please set your minimum characters lower than your maximum."
           
           elif min_char + 10 > max_char:
               context['error'] = "Please increase the range to at least 10 between your minimum and maximum characters." """   
           
           # Call generator function and eventually give result context
           if rhyme_scheme == "ABAB":
               context['result'] = "\n".join(generate_rhyme_abab_poetry(lines, state_size, 0, 140))
           elif rhyme_scheme == "AABB":
               context['result'] = "\n".join(generate_rhyme_aabb_poetry(lines, state_size, 0, 140))
           elif rhyme_scheme == "A":
               context['result'] = "\n".join(generate_rhyme_a_poetry(lines, state_size, 0, 140))
           elif rhyme_scheme == "AAA":
               context['result'] = "\n".join(generate_rhyme_aaa_poetry(lines, state_size, 0, 140))
           return context
    def validation(self, state_size, lines, rhyme_scheme): # Removed min_char, max_char,  for later implementation
        """try:
            min_char = int(min_char)
        except:
            return False
        try:
            max_char = int(max_char)
        except:
            return False"""
        try:
            state_size = int(state_size)
        except:
            return False
        try:
            lines = int(lines)
        except:
            return False
        possible_schemes = ["ABAB","AABB","AAA","ABBA","AABBA","A"]
        possible_states = [1, 2]
        
        try:
            assert rhyme_scheme in possible_schemes
        except:
            return False
        try:
            assert state_size in possible_states
        except:
            return False
        """ try:
            assert min_char >= 0 and min_char <= 100
            assert max_char >= 40 and max_char <= 140
        except:
            return False"""
        try:
            assert lines >= 4 and lines <= 40
        except:
            return False
        return True
    
class AboutPageView(TemplateView):
    template_name = "about.html"
