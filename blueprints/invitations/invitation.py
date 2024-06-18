from flask import Blueprint, request, jsonify,redirect,render_template,session,url_for
from blueprints.invitations.models import Invitation,Couple,Image,Guest
from blueprints.decorators import login_required
import base64
from app import db


invitation=Blueprint('invitation',__name__,template_folder='templates')

@invitation.route('/create')
@login_required
def invitation_create():
   return render_template('invitation_create.html')


@invitation.route('/details',methods=['POST'])
@login_required
def details():
    place=request.form['place']
    marriage_date=request.form['marriage_date']
    marriage_time=request.form['marriage_time']
    invitation=Invitation(user_id=session['user_id'],place=place,
                          marriage_date=marriage_date,marriage_time=marriage_time)
    db.session.add(invitation)
    db.session.commit()
    session['marriage_id']=invitation.id
    return redirect('/invitation/groom_details')


@invitation.route('/couple_details',methods=['POST'])
@login_required
def couple_details():
   if 'groom_name' not in request.form:
      name=request.form['bride_name']
      groom_bride=False
   else:
      name=request.form['groom_name']
      groom_bride=True
   qualification=request.form['qualification']
   dob=request.form['dob']
   relative1=request.form['relative1']
   relation1=request.form['relation1']
   relative2=request.form['relative2']
   relation2=request.form['relation2']
   relative3=request.form['relative3']
   relation3=request.form['relation3']
   image=request.files['image']
   couple=Couple(invitation_id=session['marriage_id'],name=name,
                 qualification=qualification,dob=dob,relative1=relative1,
                 relation1=relation1,relative2=relative2,relation2=relation2,
                 relative3=relative3,relation3=relation3,groom_bride=groom_bride,image=image.read())
   db.session.add(couple)
   db.session.commit()
   if groom_bride:
      return redirect('/invitation/bride_details')
   else:
      return redirect('/invitation/images')


@invitation.route('/images')
@login_required
def images():
     return render_template('invitation_images.html')
  

@invitation.route('/groom_details')
@login_required
def groom_details():
     return render_template('invitation_groom_details.html')


@invitation.route('/bride_details')
@login_required
def bride_details():
     return render_template('invitation_bride_details.html')
  
  
@invitation.route('/upload',methods=['POST'])
@login_required
def upload():
   if 'images' not in request.files:
      return redirect('/invitation/images')
   files = request.files.getlist('images')
   for file in files:
      if file:
         image=Image(invitation_id=session['marriage_id'],image=file.read())
         db.session.add(image)
   db.session.commit()
   return redirect('/invitation/view/'+str(session['marriage_id']))  


@invitation.route('/view/<invitation_id>')
def view(invitation_id):
   details=Invitation.query.filter_by(id=invitation_id).first()
   groom_details=Couple.query.filter_by(invitation_id=invitation_id,groom_bride=True).first()
   bride_details=Couple.query.filter_by(invitation_id=invitation_id,groom_bride=False).first()
   images=Image.query.filter_by(invitation_id=invitation_id).all()
   for image in images:
      image.image=base64.b64encode(image.image).decode('utf-8')
   groom_image=base64.b64encode(groom_details.image).decode('utf-8')
   bride_image=base64.b64encode(bride_details.image).decode('utf-8')
   json_details={'place':details.place,'marriage_date':details.marriage_date,'marriage_time':str(details.marriage_time)[:-3],
                 'groom_name':groom_details.name,'groom_qualification':groom_details.qualification,
                 'groom_dob':groom_details.dob,'groom_relative1':groom_details.relative1,'groom_relation1':groom_details.relation1,
                 'groom_relative2':groom_details.relative2,'groom_relation2':groom_details.relation2,
                 'groom_relative3':groom_details.relative3,'groom_relation3':groom_details.relation3,
                 'bride_name':bride_details.name,'bride_qualification':bride_details.qualification,'bride_dob':bride_details.dob,
                 'bride_relative1':bride_details.relative1,'bride_relation1':bride_details.relation1,'bride_relative2':bride_details.relative2,
                 'bride_relation2':bride_details.relation2,'bride_relative3':bride_details.relative3,'bride_relation3':bride_details.relation3,
                 'groom_image':groom_image,'bride_image':bride_image,'images':images}
   
   return render_template('invitation_card.html',details=json_details)

@invitation.route('/rvsp',methods=['POST'])
def rvsp():
   name=request.form['name']
   phone=request.form['phone']
   guests_count=request.form['guests_count']
   attending=request.form['attending']
   message=request.form['message']
   invitation_id=request.form['invitation_id']
   guest=Guest(invitation_id=invitation_id,name=name,phone=phone,guests_count=guests_count,attending=attending,message=message)
   db.session.add(guest)
   db.session.commit()
   return redirect('/invitation/view/'+invitation_id)


@invitation.route('/viewcards')
def viewcards():
   invitations=Invitation.query.filter_by(user_id=session['user_id']).all()
   couple_details=[]
   for invitation in invitations:
      groom_details=Couple.query.filter_by(invitation_id=invitation.id,groom_bride=True).first()
      bride_details=Couple.query.filter_by(invitation_id=invitation.id,groom_bride=False).first()
      couple_details.append({'id':invitation.id,'groom_name':groom_details.name,'bride_name':bride_details.name,'marriage_date':invitation.marriage_date})
   return render_template('user_viewcards.html',data=couple_details)


@invitation.route('/viewguests/<invitation_id>')
def viewguests(invitation_id):
   guests=Guest.query.filter_by(invitation_id=invitation_id).all()
   guests_details=[]
   for guest in guests:
      guests_details.append({'name':guest.name,'phone':guest.phone,'guests_count':guest.guests_count,'attending':guest.attending,'message':guest.message})
   return render_template('user_viewguests.html',data=guests_details)