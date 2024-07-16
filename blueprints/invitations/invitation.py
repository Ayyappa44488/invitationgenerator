from flask import (Blueprint, request, jsonify,
                   redirect,render_template,session,url_for)
from blueprints.invitations.models import Invitation,Couple,Image,Guest,Relative,LoveStory
from blueprints.decorators import login_required
import base64
import json
from app import db
from blueprints.invitations.qr_code import qr_generator
from blueprints.invitations.ai import story_generation
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
                          marriage_date=marriage_date,
                          marriage_time=marriage_time)

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
      session['groom_bride']=False
   else:
      name=request.form['groom_name']
      session['groom_bride']=True
      groom_bride=True

   qualification=request.form['qualification']
   dob=request.form['dob']
   relatives_count=request.form['relatives_count']
   image=request.files['image']

   couple=Couple(invitation_id = session['marriage_id'],
                 name = name,qualification = qualification,
                 dob = dob,groom_bride=groom_bride,
                 image=image.read()
                 )

   db.session.add(couple)
   db.session.commit()
   session['couple_id']=couple.id

   if groom_bride:
      return redirect(url_for('invitation.groom_relatives',
                              relatives_count=relatives_count))
   else:
      return redirect('/invitation/bride_relatives/'+relatives_count)


@invitation.route('/relatives_details',methods=['POST'])
def relatives_details():
   for i in range(len(request.form)//2-1):
      
      name=request.form['relative'+str(i)]
      relation=request.form['relation'+str(i)]
      image=request.files['image'+str(i)]
      couple_id=session['couple_id']

      relative=Relative(couple_id=couple_id,name=name,
                        relation=relation,image=image.read()
                        )

      db.session.add(relative)
      db.session.commit()
   if session['groom_bride']:
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


@invitation.route('/groom_relatives/<int:relatives_count>')
def groom_relatives(relatives_count):
   return render_template('groom_relatives.html',
                          relative_count=relatives_count,
                          api_url='/invitation/relatives_details',
                          name='Groom')


@invitation.route('/bride_relatives/<int:relatives_count>')
def bride_relatives(relatives_count):
   return render_template('groom_relatives.html',
                          relative_count=relatives_count,
                          api_url='/invitation/relatives_details',
                          name='Bride')


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
                     image=file.read())

         db.session.add(image)

   db.session.commit()
   marriage_id=session['marriage_id']
   session.pop('groom_bride', None)
   session.pop('couple_id', None)
   session.pop('marriage_id', None)
   return redirect('/invitation/templates/'+str(marriage_id))  


@invitation.route('/view/<invitation_id>/<template_id>')
def view(invitation_id,template_id):
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
   
   love_story=LoveStory.query.filter_by(invitation_id=invitation_id,
                                        deleted_at=None).first()

   for image in images:
      image.image=base64.b64encode(image.image).decode('utf-8')
   groom_image=base64.b64encode(groom_details.image).decode('utf-8')
   bride_image=base64.b64encode(bride_details.image).decode('utf-8')
   for relative in groom_relatives:
      relative.image=base64.b64encode(relative.image).decode('utf-8')
   for relative in bride_relatives:
      relative.image=base64.b64encode(relative.image).decode('utf-8')
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
      'images': images,
      'first_meet': love_story.first_meet,
      'first_date': love_story.first_date,
      'proposal': love_story.proposal,
      'engagement': love_story.engagement,
      'first_meet_date': love_story.first_meet_date,
      'first_date_date': love_story.first_date_date,
      'proposal_date': love_story.proposal_date,
      'engagement_date': love_story.engagement_date
   }
   
   return render_template(f'invitation_card{template_id}.html',details=json_details)


@invitation.route('/rvsp',methods=['POST'])
def rvsp():
   name = request.form['name']
   phone = request.form['phone']
   guests_count = request.form['guests_count']
   attending = request.form['attending']
   message = request.form['message']
   invitation_id = request.form['invitation_id']
   template_id = request.form['template_id']

   guest=Guest(invitation_id = invitation_id,name = name,phone = phone,
               guests_count = guests_count,attending = attending,
               message = message)

   db.session.add(guest)
   db.session.commit()

   return redirect(f'/invitation/view/{invitation_id}/{template_id}')


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
         'marriage_date': invitation.marriage_date,
         'template_selected': invitation.template_selected
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
   love_story=LoveStory.query.filter_by(invitation_id=invitation_id,
                                        deleted_at=None).first()
   if love_story:
      love_story.deleted_at=db.func.now()

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

   groom_relatives=Relative.query.filter_by(couple_id=groom_details.id,
                                      deleted_at=None).all()

   bride_relatives=Relative.query.filter_by(couple_id=bride_details.id,
                                       deleted_at=None).all()

   for image in images:
      image.image=base64.b64encode(image.image).decode('utf-8')

   groom_image=base64.b64encode(groom_details.image).decode('utf-8')
   bride_image=base64.b64encode(bride_details.image).decode('utf-8')

   for relative in groom_relatives:
      relative.image=base64.b64encode(relative.image).decode('utf-8')

   for relative in bride_relatives:
      relative.image=base64.b64encode(relative.image).decode('utf-8')

   json_details={
      'place': details.place,
      'marriage_date': details.marriage_date,
      'marriage_time': str(details.marriage_time)[:-3],
      'groom_name': groom_details.name,
      'groom_qualification': groom_details.qualification,
      'groom_dob': groom_details.dob,
      'groom_relatives': groom_relatives,
      'groom_relatives_count': len(groom_relatives),
      'bride_name': bride_details.name,
      'bride_qualification': bride_details.qualification,
      'bride_dob': bride_details.dob,
      'bride_relatives': bride_relatives,
      'bride_relatives_count': len(bride_relatives),
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
   a=[]
   for i in request.form:
      if i.isdigit():
            a.append(i)
   
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
   groom_details=Couple.query.filter_by(invitation_id=invitation_id,
                                        groom_bride=True,deleted_at=None
                                        ).first()

   if 'groom-pic' in request.files and request.files['groom-pic'].filename!='':
      groom_image=request.files['groom-pic']
      groom_image=groom_image.read()
      groom_details.image=groom_image

   groom_details.name=groom_name
   groom_details.qualification=groom_qualification
   groom_details.dob=groom_dob

   bride_name=request.form['bride-name']
   bride_qualification=request.form['bride-qualification']
   bride_dob=request.form['bride-dob']
   bride_details=Couple.query.filter_by(invitation_id=invitation_id,
                                        groom_bride=False,deleted_at=None
                                        ).first()
   if 'bride-pic' in request.files and request.files['bride-pic'].filename!='':
      bride_image=request.files['bride-pic']
      bride_image=bride_image.read()
      bride_details.image=bride_image


   bride_details.name=bride_name
   bride_details.qualification=bride_qualification
   bride_details.dob=bride_dob
   
   for i in a:
      relative_name=request.form[i]
      relatiom=request.form['relation'+i]
      relative=Relative.query.filter_by(id=int(i),deleted_at=None).first()
      if 'relative_pic'+i in request.files and request.files['relative_pic'+i].filename!='':
         relative_image=request.files['relative_pic'+i]
         relative_image=relative_image.read()
         relative.image=relative_image
      relative.name=relative_name
      relative.relation=relatiom

   if 'new-couple-pic' in request.files:
      files = request.files.getlist('new-couple-pic')

      for file in files:
         if file:
            image=Image(invitation_id=invitation_id,
                        image=file.read())

            db.session.add(image)

   db.session.commit()
   session.pop('invitation_id')

   return redirect('/invitation/view/'+str(invitation_id))


@invitation.route('/templates/<invitation_id>')
def templates(invitation_id):
   session['invitation_id']=invitation_id
   return render_template('invitation_web_templates.html',invitation_id=invitation_id)


@invitation.route('/template/<template_id>')
def template(template_id):
   invitation_id=session['invitation_id']
   invitation=Invitation.query.filter_by(id=invitation_id).first()
   invitation.template_selected=template_id
   db.session.commit()
   # session.pop('invitation_id')
   filename=f'static/images/invitation/qrcodes/{invitation_id}.{template_id}.png'
   url=f'http://127.0.0.1:5000/invitation/view/{invitation_id}/{template_id}'
   qr_generator(url,filename)
   return render_template('qr_display.html' ,url=url ,filename=filename)


@invitation.route('/love_story')
def love_story():
   description="we met in coffe shop in bhimavaram. we gone to a date in perupalem beach and then i proposed her in bhimavaram and then  got engaged with her"
   results=story_generation(description)
   if len(results)<8:
      return jsonify({'status': 'failure'})
   invitation_id=11
   love_story=LoveStory(invitation_id=invitation_id,first_meet=results[0],
                        first_date=results[1],proposal=results[2],
                        engagement=results[3],first_meet_date=results[4],
                        first_date_date=results[5],proposal_date=results[6],
                        engagement_date=results[7])
   
   db.session.add(love_story)
   db.session.commit()
   
   return jsonify({'status': 'success'})
