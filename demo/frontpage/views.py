from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# from tables import BillboardTable
from frontpage.models import BillboardData
from frontpage import forms
import pickle
import re
# other packages
from sklearn.pipeline import make_pipeline
from lime import lime_text

def index(request):
    form = forms.lyricsForModel()
    context = {
        'form':form
    }
    if request.method == 'POST':
        form = forms.lyricsForModel(request.POST)
        verbose = True
        if form.is_valid():
            lyrics = form.cleaned_data['text']
            if verbose:
                exp = lime_lyrics(lyrics)
                html = exp.as_html()
                #return HttpResponse(html)
                context['my_html'] = html
                return render(request,
                              'frontpage/index.html',
                              context = context)
            else:
                pred = lime_lyrics(lyrics, verbose = False)
                context['negative'],context['positive'] = pred[0,0],pred[0,1]
                return render(request,
                              'frontpage/billboard.html',
                              context)
    return render(request,
                  'frontpage/index.html',
                  context=context)

def lime_lyrics(lyrics,verbose = True):
    '''
    Funtion that computes output on billboard.html
    '''
    print(repr(lyrics))
    print('____________________' + lyrics + '____________________')
    with open('model.pkl','rb') as fp:
        model = pickle.load(fp)
    with open('counter.pkl','rb') as fp:
        counter = pickle.load(fp)
    if verbose:
        # one bug of lime not fixed yet
        # sklearn 0.20.0
        tokenizer = lambda doc: re.compile(r"(?u)\b\w\w+\b").findall(doc)
        #raise ValueError('Not implemented')
        pipe = make_pipeline(counter,model)
        class_names = ['Not on billboard','On billboard']
        explainer = lime_text.LimeTextExplainer(class_names=class_names,
                                                split_expression=tokenizer)
     
        
        exp = explainer.explain_instance(lyrics,pipe.predict_proba,
                                         num_features = 12)
        return exp
    else:
        inst = counter.transform([lyrics])
        pred = model.predict_proba(inst)
        return pred

def lime_lyrics2(lyrics):
    lyrics = lyrics.replace('\n','')
    with open('model.pkl','rb') as fp:
        model = pickle.load(fp)
    with open('counter.pkl','rb') as fp:
        counter = pickle.load(fp)
    pipe = make_pipeline(counter,model)
    class_names = ['Not on billboard','On billboard']
    explainer = lime_text.LimeTextExplainer(class_names=class_names)  
    exp = explainer\
    .explain_instance(lyrics,
                      pipe.predict_proba,
                     num_features = 12)
    return exp
def billboard(request):
    table = BillboardData.objects.all()
    form = forms.lyricsForModel()
    context = {'table':table,
               'form':form}
    
    
    if request.method == 'POST':
        form = forms.lyricsForModel(request.POST)
        verbose = True
        if form.is_valid():
            lyrics = form.cleaned_data['text']
            if verbose:
                exp = lime_lyrics(lyrics)
                html = exp.as_html()
                return HttpResponse(html)
            else:
                pred = lime_lyrics(lyrics, verbose = False)
                context['negative'],context['positive'] = pred[0,0],pred[0,1]
                return render(request,
                              'frontpage/billboard.html',
                              context)
    return render(request,'frontpage/billboard.html',
                  context)