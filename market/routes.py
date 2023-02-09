from flask import render_template, url_for, redirect, send_from_directory, flash, request
from market import app
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, ComprarItemForm, VenderItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    comprar_form = ComprarItemForm()
    vender_form = VenderItemForm()
    if request.method == "POST":
        # Logica comprar item
        comprar_item = request.form.get('comprar_item')
        comprar_item_object = Item.query.filter_by(name=comprar_item).first()
        if comprar_item_object:
            if current_user.can_purchase(comprar_item_object):
                comprar_item_object.comprar(current_user)
                flash(f'Parabéns! você comprou {comprar_item_object.name} por {comprar_item_object.price}',
                      category='success')
            else:
                flash(
                    f"Infelizmente, você não tem dinheiro suficiente para comprar o produto: {comprar_item_object.name}",
                    category='danger')

        # Logica vender item
        vender_item = request.form.get('vender_item')
        vender_item_object = Item.query.filter_by(name=vender_item).first()
        if vender_item_object:
            if current_user.can_sell(vender_item_object):
                vender_item_object.vender(current_user)
                flash(f'Parabéns! você vendeu {vender_item_object.name} de volta para o mercado!', category='success')
            else:
                flash(
                    f'Algo de errado aconteceu com {vender_item_object.name} enquanto vendia de volta para o mercado!',
                    category='danger')

        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        itens_de_propriedade = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, comprar_form=comprar_form,
                               itens_de_propriedade=itens_de_propriedade, vender_form=vender_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        user_create = User(username=form.username.data,
                           email=form.email.data,
                           password=form.password1.data)
        db.session.add(user_create)
        db.session.commit()
        login_user(user_create)
        flash(f'Conta criada com sucesso! você esta logado como: {user_create.username}', category='success')

        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Ocorreu um erro ao criar o Usuário: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        logar_usuario = User.query.filter_by(username=form.username.data).first()
        if logar_usuario and logar_usuario.check_password_correction(
                login_password=form.password.data
        ):
            login_user(logar_usuario)
            flash(f'Sucesso! você está logado como: {logar_usuario.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Usuário ou senha não encontrado! Por favor tente novamente.', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('Voce efetuou o logout do sistema.', category='info')
    return redirect(url_for('home_page'))
