import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Upload, ChatHistory
from .utils import *
import numpy as np
import faiss
from django.contrib import messages
from .Ai_conf import *
from cohere import client
co = client.Client(os.getenv("API_KEY"))

# Create your views here.
def upload(request):
    answer = ""
    context = ""
    text = ""
    base_name = ""
    doc = None
    
    
    if request.method == "POST":
        if 'file' in request.FILES:
            # ⬇️ Handle upload
            uploaded_file = request.FILES['file']
            doc = Upload.objects.create(file=uploaded_file)
            path = doc.file.path
            
            if path.endswith('.pdf'):
                text = extract_pdf(path)
            elif path.endswith('.docx'):
                text = extract_docx(path)
            else:
                messages.warning(request, 'Invalid file type. Please upload a PDF or DOCX file.')
                return HttpResponseRedirect(request.path_info)
            
            base_name = os.path.splitext(os.path.basename(doc.file.name))[0]
            save_to_faiss_and_text(text, base_name)
            doc.extract = text
            doc.save()
            messages.success(request, "File uploaded and processed.")
            return redirect("upload")

        elif 'question' in request.POST:
            # ⬇️ Handle question
            question = request.POST.get('question')
            doc_id = request.POST.get('document')
            doc = Upload.objects.get(id=doc_id)
            base_name = os.path.splitext(os.path.basename(doc.file.name))[0]
            answer, context = process_question(question, base_name)
           
            # ✅ Save the chat history
            ChatHistory.objects.create(
                     document=doc,
                   question=question,
                    answer=answer
            )
             # ✅ Save values in session to persist across redirect
            request.session['answer'] = answer
            request.session['context'] = context
            request.session['doc_id'] = doc.id
            return redirect("upload")
            
                # ✅ GET request or after redirect
    answer = request.session.pop('answer', '')
    context = request.session.pop('context', '')
    doc_id = request.session.pop('doc_id', None)
    doc = Upload.objects.get(id=doc_id) if doc_id else None


    docs = Upload.objects.all()
    history = ChatHistory.objects.filter(document=doc).order_by('-asked_at') if doc else []
    return render(request, 'core/core.html', {
        'docs': docs,
        'answer': answer,
        'context': context,
        'history': history,
        'history': history,
    })



def delete_document(request, pk):
    
    doc = get_object_or_404(Upload, pk=pk)
    base_name = os.path.splitext(os.path.basename(doc.file.name))[0]

    paths = [
        f"media/vectors/{base_name}.index",
        f"media/texts/{base_name}.txt",
        doc.file.path
    ]
    for p in paths:
        if os.path.exists(p):
            os.remove(p)
    doc.delete()
    messages.success(request, "Document deleted successfully.")
    return redirect("upload")
