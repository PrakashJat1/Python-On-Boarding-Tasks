from django.urls import path
from . import views

urlpatterns = [
    
    #address
    path("address-page/",views.address_page_view,name="address-page"),
    path('add-address/',views.add_address_view,name="add-address"),
    path('edit-address/<int:address_id>',views.edit_address_view,name="edit-address"),
    path('delete-address/<int:address_id>',views.delete_address_view,name="delete-address"),
    
    #profile
    path('profile-page/',views.profile_page_view,name="profile-page"),
    path('edit-profile-picture/<int:id>',views.edit_profile_picture_view,name="edit-profile-picture"),
    path('edit-profile/<int:id>',views.edit_profile_view,name="edit-profile")
    

]
