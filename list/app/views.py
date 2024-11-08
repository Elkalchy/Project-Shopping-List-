from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import Category,Item
from django.shortcuts import get_object_or_404
from django.contrib import messages

# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password)
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            print( "Nom d'utilisateur ou mot de passe incorrect.")
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')



def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Vérifier que les mots de passe correspondent
        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('signup')

        # Vérifier que l'email n'est pas déjà utilisé
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect('signup')

        # Vérifier si le nom d'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return redirect('signup')

        # Créer l'utilisateur
        user = User(username=username, email=email)
        user.set_password(password1)
        user.save()
        
        messages.success(request, "Votre compte a été créé avec succès. Vous pouvez vous connecter.")
        return redirect('login')

    return render(request, 'signup.html')



def index(request):
    itemss=Item.objects.filter(user=request.user)
    return render(request,'index.html',{'items':itemss})



def edit_item(request, list_id):
    itemss = get_object_or_404(Item, id=list_id)
    
    if request.method == "POST":
        name = request.POST.get('name')
        quantite = request.POST.get('quantite')
        categorie = request.POST.get('categorie')
        status = request.POST.get('status')
        
        # التأكد من أن جميع الحقول مدخلة بشكل صحيح
        if not all([name, quantite, categorie, status]):
            # إعادة توجيه إلى نفس الصفحة مع رسالة خطأ إذا كانت البيانات غير مكتملة
            return render(request, 'edit_item.html', {'itemss': itemss, 'error': 'الرجاء ملء جميع الحقول'})

        # التحقق مما إذا كانت الفئة موجودة بالفعل في قاعدة البيانات
        catog, _ = Category.objects.get_or_create(name=categorie)

        # تحديث حقول العنصر
        itemss.name = name
        itemss.quantity = quantite
        itemss.status = status
        itemss.category = catog

        # حفظ العنصر
        itemss.save()

        # إعادة التوجيه إلى الصفحة الرئيسية بعد تعديل العنصر
        return redirect('index')
    
    return render(request, 'edit_item.html', {'itemss': itemss})

def del_item(request, list_id):
    itemss = get_object_or_404(Item, id=list_id)

    # Vérifier que l'utilisateur connecté est le propriétaire de l'élément
    if itemss.user == request.user:
        itemss.delete()
        return redirect('index')  # Redirection vers l'index après la suppression
    else:
        # Rediriger vers l'index avec un message d'erreur ou afficher un message
        return redirect('index')
    
    

def add_item(request):
    if request.method == "POST":
        name = request.POST.get('name')
        quantite = request.POST.get('quantite')
        categorie = request.POST.get('categorie')
        status = request.POST.get('status')

        # التحقق مما إذا كانت الفئة موجودة بالفعل في قاعدة البيانات
        catog, created = Category.objects.get_or_create(name=categorie)

        # إنشاء العنصر وربطه بالفئة
        items = Item(name=name, quantity=quantite, status=status, category=catog, user=request.user) 

        # حفظ العنصر
        items.save()

        # إعادة التوجيه إلى الصفحة الرئيسية بعد إضافة العنصر
        return redirect('index')

    return render(request, 'add_item.html')