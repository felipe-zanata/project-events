from django.shortcuts import render,redirect
from .forms import LoginForm, CadastroForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

# Create your views here.
def logar(request):

    if request.user.is_authenticated:
        return redirect('listar_eventos')

    if request.method == 'GET':
        form = LoginForm()
    elif request.method =='POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            usuario = form.cleaned_data['username']
            senha = form.cleaned_data['password']
            user = authenticate(request, username=usuario, password=senha)

            if user is not None:
                login(request, user)
                return redirect('listar_eventos')
            else:
                form.add_error(None, 'Usuario ou senhas Incorretos')

    return render(request,'login.html',{'form': form})
        
def logout_view(request):
    logout(request)
    return redirect('/usuarios/logar')
    
def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/usuarios/logar')
    else:    
        form = CadastroForm()    
    return render(request, 'cadastro.html', {'form': form})

class UserListView(ListView):
    model = User
    template_name = 'lista_usuario.html'
    context_object_name = 'users'

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        id = request.POST.get('user_id')
        print(id)
        try:
            pedido = User.objects.get(pk=id)
            pedido.save()
            pedido.delete()
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'User with id {id} does not exist'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'message': 'Users deletados com sucesso'})