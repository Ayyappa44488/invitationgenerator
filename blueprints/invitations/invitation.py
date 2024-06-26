from flask import (Blueprint, request, jsonify,
                   redirect,render_template,session,url_for)
from blueprints.invitations.models import Invitation,Couple,Image,Guest,Relative
from blueprints.decorators import login_required
import base64
import json
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

   couple=Couple(invitation_id = session['marriage_id'],
                 name = name,qualification = qualification,
                 dob = dob,relative1 = relative1,
                 relation1 = relation1,relative2 = relative2,
                 relation2 = relation2,relative3=relative3,
                 relation3=relation3,groom_bride=groom_bride,
                 image=image.read()
                 )

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
         image=Image(invitation_id=session['marriage_id'],
                     image=file.read()
                     )

         db.session.add(image)

   db.session.commit()

   return redirect('/invitation/view/'+str(session['marriage_id']))  


@invitation.route('/view/<invitation_id>')
def view(invitation_id):
   details=Invitation.query.filter_by(id=invitation_id
                                      ,deleted_at=None).first()

   groom_details=Couple.query.filter_by(invitation_id=invitation_id,
                                        groom_bride=True,deleted_at=None
                                        ).first()

   bride_details=Couple.query.filter_by(invitation_id=invitation_id,
                                        groom_bride=False,deleted_at=None
                                        ).first()

   images=Image.query.filter_by(invitation_id=invitation_id,
                                deleted_at=None).all()

   groom_relatives=Relative.query.filter_by(couple_id=groom_details.id,
                                      deleted_at=None).all()

   bride_relatives=Relative.query.filter_by(couple_id=bride_details.id,
                                       deleted_at=None).all()

   for image in images:
      image.image=base64.b64encode(image.image).decode('utf-8')
   groom_image=base64.b64encode(groom_details.image).decode('utf-8')
   bride_image=base64.b64encode(bride_details.image).decode('utf-8')
   json_details={
      'place': details.place,
      'marriage_date': details.marriage_date,
      'marriage_time': str(details.marriage_time)[:-3],
      'groom_name': groom_details.name,
      'groom_qualification': groom_details.qualification,
      'groom_dob': groom_details.dob,
      'groom_relatives': groom_relatives,
      'bride_name': bride_details.name,
      'bride_qualification': bride_details.qualification,
      'bride_dob': bride_details.dob,
      'bride_relatives': bride_relatives,
      'groom_image': groom_image,
      'bride_image': bride_image,
      'images': images
   }
   
   return render_template('invitation_card.html',details=json_details)


@invitation.route('/rvsp',methods=['POST'])
def rvsp():
   name=request.form['name']
   phone=request.form['phone']
   guests_count=request.form['guests_count']
   attending=request.form['attending']
   message=request.form['message']
   invitation_id=request.form['invitation_id']

   guest=Guest(invitation_id = invitation_id,name = name,phone = phone,
               guests_count = guests_count,attending = attending,
               message = message
               )

   db.session.add(guest)
   db.session.commit()

   return redirect('/invitation/view/'+invitation_id)


@invitation.route('/viewcards')
def viewcards():
   invitations=Invitation.query.filter_by(user_id = session['user_id'],
                                          deleted_at = None
                                          ).all()

   couple_details=[]

   for invitation in invitations:
      groom_details=Couple.query.filter_by(invitation_id = invitation.id,
                                           groom_bride = True,deleted_at = None
                                           ).first()

      bride_details=Couple.query.filter_by(invitation_id = invitation.id,
                                           groom_bride = False,deleted_at = None
                                           ).first()

      couple_details.append({
         'id': invitation.id,
         'groom_name': groom_details.name,
         'bride_name': bride_details.name,
         'marriage_date': invitation.marriage_date
      })

   return render_template('user_viewcards.html',data=couple_details)


@invitation.route('/viewguests/<invitation_id>')
def viewguests(invitation_id):
   guests=Guest.query.filter_by(invitation_id = invitation_id,
                                deleted_at = None
                                ).all()

   guests_details=[]

   for guest in guests:
      guests_details.append({
         'name': guest.name,
         'phone': guest.phone,
         'guests_count': guest.guests_count,
         'attending': guest.attending,
         'message': guest.message
      })

   return render_template('user_viewguests.html',data=guests_details)


@invitation.route('/delete/<invitation_id>')
def delete(invitation_id):
   invitation=Invitation.query.filter_by(id = invitation_id,
                                         deleted_at = None
                                         ).first()

   invitation.deleted_at=db.func.now()
   images=Image.query.filter_by(invitation_id = invitation_id,
                                deleted_at = None
                                ).all()

   for image in images:
      image.deleted_at=db.func.now()

   guests=Guest.query.filter_by(invitation_id = invitation_id,
                                deleted_at = None
                                ).all()

   for guest in guests:
      guest.deleted_at=db.func.now()

   couple_details=Couple.query.filter_by(invitation_id = invitation_id,
                                         deleted_at = None
                                         ).all()

   for couple in couple_details:
      couple.deleted_at=db.func.now()

   db.session.commit()

   return redirect('/invitation/viewcards')


@invitation.route('edit/<invitation_id>')
def edit(invitation_id):

   details=Invitation.query.filter_by(id=invitation_id
                                      ,deleted_at=None
                                      ).first()

   groom_details=Couple.query.filter_by(invitation_id=invitation_id,
                                        groom_bride=True,deleted_at=None
                                        ).first()

   bride_details=Couple.query.filter_by(invitation_id=invitation_id,
                                        groom_bride=False,deleted_at=None
                                        ).first()

   images=Image.query.filter_by(invitation_id=invitation_id,
                                deleted_at=None
                                ).all()

   for image in images:
      image.image=base64.b64encode(image.image).decode('utf-8')

   groom_image=base64.b64encode(groom_details.image).decode('utf-8')
   bride_image=base64.b64encode(bride_details.image).decode('utf-8')
   json_details={
      'place': details.place,
      'marriage_date': details.marriage_date,
      'marriage_time': str(details.marriage_time)[:-3],
      'groom_name': groom_details.name,
      'groom_qualification': groom_details.qualification,
      'groom_dob': groom_details.dob,
      'groom_relative1': groom_details.relative1,
      'groom_relation1': groom_details.relation1,
      'groom_relative2': groom_details.relative2,
      'groom_relation2': groom_details.relation2,
      'groom_relative3': groom_details.relative3,
      'groom_relation3': groom_details.relation3,
      'bride_name': bride_details.name,
      'bride_qualification': bride_details.qualification,
      'bride_dob': bride_details.dob,
      'bride_relative1': bride_details.relative1,
      'bride_relation1': bride_details.relation1,
      'bride_relative2': bride_details.relative2,
      'bride_relation2': bride_details.relation2,
      'bride_relative3': bride_details.relative3,
      'bride_relation3': bride_details.relation3,
      'groom_image': groom_image,
      'bride_image': bride_image,
      'images': images
   }
   session['invitation_id']=invitation_id

   return render_template('invitation_edit.html',details=json_details)


@invitation.route('/delete_image',methods=['POST'])
def delete_image():
   image_id=request.json['id']
   image=Image.query.filter_by(id=image_id).first()
   image.deleted_at=db.func.now()
   db.session.commit()

   return jsonify({'status': 'success'})


@invitation.route('/update_weddingdetails',methods=['POST'])
def update_weddingdetails():
   place=request.form['place']
   marriage_date=request.form['date']
   marriage_time=request.form['time']
   invitation_id=session['invitation_id']

   invitation=Invitation.query.filter_by(id=invitation_id).first()
   invitation.place=place
   invitation.marriage_date=marriage_date
   invitation.marriage_time=marriage_time

   groom_name=request.form['groom-name']
   groom_qualification=request.form['groom-qualification']
   groom_dob=request.form['groom-dob']
   groom_relative1=request.form['groom-relative1']
   groom_relation1=request.form['groom-relation1']
   groom_relative2=request.form['groom-relative2']
   groom_relation2=request.form['groom-relation2']
   groom_relative3=request.form['groom-relative3']
   groom_relation3=request.form['groom-relation3']
   if 'groom-pic' in request.files:
      groom_image=request.files['groom-pic']
      groom_image=groom_image.read()

   groom_details=Couple.query.filter_by(invitation_id=invitation_id,
                                        groom_bride=True,deleted_at=None
                                        ).first()

   groom_details.name=groom_name
   groom_details.qualification=groom_qualification
   groom_details.dob=groom_dob
   groom_details.relative1=groom_relative1
   groom_details.relation1=groom_relation1
   groom_details.relative2=groom_relative2
   groom_details.relation2=groom_relation2
   groom_details.relative3=groom_relative3
   groom_details.relation3=groom_relation3
   if 'groom-pic' in request.files:
      groom_details.image=groom_image

   bride_name=request.form['bride-name']
   bride_qualification=request.form['bride-qualification']
   bride_dob=request.form['bride-dob']
   bride_relative1=request.form['bride-relative1']
   bride_relation1=request.form['bride-relation1']
   bride_relative2=request.form['bride-relative2']
   bride_relation2=request.form['bride-relation2']
   bride_relative3=request.form['bride-relative3']
   bride_relation3=request.form['bride-relation3']
   if 'bride-pic' in request.files:
      bride_image=request.files['bride-pic']
      bride_image=bride_image.read()

   bride_details=Couple.query.filter_by(invitation_id=invitation_id,
                                        groom_bride=False,deleted_at=None
                                        ).first()

   bride_details.name=bride_name
   bride_details.qualification=bride_qualification
   bride_details.dob=bride_dob
   bride_details.relative1=bride_relative1
   bride_details.relation1=bride_relation1
   bride_details.relative2=bride_relative2
   bride_details.relation2=bride_relation2
   bride_details.relative3=bride_relative3
   bride_details.relation3=bride_relation3
   if 'bride-pic' in request.files:
      bride_details.image=bride_image

   if 'new-couple-pic' in request.files:
      files = request.files.getlist('new-couple-pic')

      for file in files:
         if file:
            image=Image(invitation_id=invitation_id,
                        image=file.read()
                        )

            db.session.add(image)

   db.session.commit()
   session.pop('invitation_id')

   return redirect('/invitation/view/'+str(invitation_id))
                                                 