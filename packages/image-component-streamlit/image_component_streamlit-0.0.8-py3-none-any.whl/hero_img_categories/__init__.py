import os
import streamlit.components.v1 as components

_RELEASE = True  

if not _RELEASE:
  _image_component_streamlit = components.declare_component(
      
      "image_component_streamlit",

      url="http://localhost:3001",
  )
else:
   
  parent_dir = os.path.dirname(os.path.abspath(__file__))
  build_dir = os.path.join(parent_dir, "frontend/build")
  _image_component_streamlit = components.declare_component("image_component_streamlit", path=build_dir)

def image_component_streamlit(data=None, styles=None, hideToolTip=None, key=None, default=None):
   
  component_value = _image_component_streamlit(data=data, styles=styles, hideToolTip=hideToolTip, key=key, default=default)

  return component_value

if not _RELEASE:
  import streamlit as st

  #   heroes = [
  #   {
  #     "id": 1,
  #     "heroName": "Miya",
  #     "skillUrl": "http://localhost:8501/app/static/abilities/Miya/Miya_Moon_Arrow.png",
  #     "heroUrl": "http://localhost:8501/app/static/abilities/Miya/Miya_Moon_Arrow.png"
  #   },
  #   {
  #     "id": 2,
  #     "heroName": "Miya",
  #     "skillUrl": "http://localhost:8501/app/static/abilities/Miya/Miya_Moon_Arrow.png",
  #     "heroUrl": "http://localhost:8501/app/static/abilities/Miya/Miya_Moon_Arrow.png"
  #   },
  #   {
  #     "id": 3,
  #     "heroName": "Miya",
  #     "skillUrl": "http://localhost:8501/app/static/abilities/Miya/Miya_Moon_Arrow.png",
  #     "heroUrl": "http://localhost:8501/app/static/abilities/Miya/Miya_Moon_Arrow.png"
  #   }
  # ]
    
  heroes=[
  {
    "id": 0,
    "heroName": "Layla",
    "skillUrl": "http://localhost:8501/app/static/abilities/Layla/Layla_Malefic_Bomb.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Layla.png"
  },
  {
    "id": 1,
    "heroName": "Layla",
    "skillUrl": "http://localhost:8501/app/static/abilities/Layla/Layla_Void_Projectile.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Layla.png"
  },
  {
    "id": 2,
    "heroName": "Layla",
    "skillUrl": "http://localhost:8501/app/static/abilities/Layla/Layla_Destruction_Rush.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Layla.png"
  },
  {
    "id": 3,
    "heroName": "Hanabi",
    "skillUrl": "http://localhost:8501/app/static/abilities/Hanabi/Hanabi_Ninjutsu_Equinox.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Hanabi.png"
  },
  {
    "id": 4,
    "heroName": "Hanabi",
    "skillUrl": "http://localhost:8501/app/static/abilities/Hanabi/Hanabi_Ninjutsu_Soul_Scroll.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Hanabi.png"
  },
  {
    "id": 5,
    "heroName": "Hanabi",
    "skillUrl": "http://localhost:8501/app/static/abilities/Hanabi/Hanabi_Forbidden_Jutsu_Higanbana.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Hanabi.png"
  },
  {
    "id": 6,
    "heroName": "Kimmy",
    "skillUrl": "http://localhost:8501/app/static/abilities/Kimmy/Kimmy_Energy_Transformation.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Kimmy.png"
  },
  {
    "id": 7,
    "heroName": "Kimmy",
    "skillUrl": "http://localhost:8501/app/static/abilities/Kimmy/Kimmy_Chemical_Refinement.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Kimmy.png"
  },
  {
    "id": 8,
    "heroName": "Kimmy",
    "skillUrl": "http://localhost:8501/app/static/abilities/Kimmy/Kimmy_Maximum_Charge.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Kimmy.png"
  },
  {
    "id": 9,
    "heroName": "Melissa",
    "skillUrl": "http://localhost:8501/app/static/abilities/Melissa/Melissa_Falling.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Melissa.png"
  },
  {
    "id": 10,
    "heroName": "Melissa",
    "skillUrl": "http://localhost:8501/app/static/abilities/Melissa/Melissa_Eyes_on_You.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Melissa.png"
  },
  {
    "id": 11,
    "heroName": "Melissa",
    "skillUrl": "http://localhost:8501/app/static/abilities/Melissa/Melissa_Go_Away.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Melissa.png"
  },
  {
    "id": 12,
    "heroName": "Bruno",
    "skillUrl": "http://localhost:8501/app/static/abilities/Bruno/Bruno_Volley_Shot.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Bruno.png"
  },
  {
    "id": 13,
    "heroName": "Bruno",
    "skillUrl": "http://localhost:8501/app/static/abilities/Bruno/Bruno_Flying_Tackle.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Bruno.png"
  },
  {
    "id": 14,
    "heroName": "Bruno",
    "skillUrl": "http://localhost:8501/app/static/abilities/Bruno/Bruno_Worldie.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Bruno.png"
  },
  {
    "id": 15,
    "heroName": "Granger",
    "skillUrl": "http://localhost:8501/app/static/abilities/Granger/Granger_Rhapsody.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Granger.png"
  },
  {
    "id": 16,
    "heroName": "Granger",
    "skillUrl": "http://localhost:8501/app/static/abilities/Granger/Granger_Rondo.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Granger.png"
  },
  {
    "id": 17,
    "heroName": "Granger",
    "skillUrl": "http://localhost:8501/app/static/abilities/Granger/Granger_Death_Sonata.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Granger.png"
  },
  {
    "id": 18,
    "heroName": "Edith",
    "skillUrl": "http://localhost:8501/app/static/abilities/Edith/Edith_Earth_Shatter.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Edith.png"
  },
  {
    "id": 19,
    "heroName": "Edith",
    "skillUrl": "http://localhost:8501/app/static/abilities/Edith/Edith_Onward.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Edith.png"
  },
  {
    "id": 20,
    "heroName": "Edith",
    "skillUrl": "http://localhost:8501/app/static/abilities/Edith/Edith_Divine_Retribution.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Edith.png"
  },
  {
    "id": 21,
    "heroName": "Edith",
    "skillUrl": "http://localhost:8501/app/static/abilities/Edith/Edith_Lightning_Bolt.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Edith.png"
  },
  {
    "id": 22,
    "heroName": "Karrie",
    "skillUrl": "http://localhost:8501/app/static/abilities/Karrie/Karrie_Spinning_Lightwheel.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Karrie.png"
  },
  {
    "id": 23,
    "heroName": "Karrie",
    "skillUrl": "http://localhost:8501/app/static/abilities/Karrie/Karrie_Phantom_Step.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Karrie.png"
  },
  {
    "id": 24,
    "heroName": "Karrie",
    "skillUrl": "http://localhost:8501/app/static/abilities/Karrie/Karrie_Speedy_Lightwheel.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Karrie.png"
  },
  {
    "id": 25,
    "heroName": "Claude",
    "skillUrl": "http://localhost:8501/app/static/abilities/Claude/Claude_Art_of_Thievery.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Claude.png"
  },
  {
    "id": 26,
    "heroName": "Claude",
    "skillUrl": "http://localhost:8501/app/static/abilities/Claude/Claude_Battle_Mirror_Image.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Claude.png"
  },
  {
    "id": 27,
    "heroName": "Claude",
    "skillUrl": "http://localhost:8501/app/static/abilities/Claude/Claude_Blazing_Duet.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Claude.png"
  },
  {
    "id": 28,
    "heroName": "Clint",
    "skillUrl": "http://localhost:8501/app/static/abilities/Clint/Clint_Quick_Draw.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Clint.png"
  },
  {
    "id": 29,
    "heroName": "Clint",
    "skillUrl": "http://localhost:8501/app/static/abilities/Clint/Clint_Trapping_Recoil.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Clint.png"
  },
  {
    "id": 30,
    "heroName": "Clint",
    "skillUrl": "http://localhost:8501/app/static/abilities/Clint/Clint_Grenade_Bombardment.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Clint.png"
  },
  {
    "id": 31,
    "heroName": "Irithel",
    "skillUrl": "http://localhost:8501/app/static/abilities/Irithel/Irithel_Strafe.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Irithel.png"
  },
  {
    "id": 32,
    "heroName": "Irithel",
    "skillUrl": "http://localhost:8501/app/static/abilities/Irithel/Irithel_Force_of_the_Queen.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Irithel.png"
  },
  {
    "id": 33,
    "heroName": "Irithel",
    "skillUrl": "http://localhost:8501/app/static/abilities/Irithel/Irithel_Heavy_Crossbow.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Irithel.png"
  },
  {
    "id": 34,
    "heroName": "Lesley",
    "skillUrl": "http://localhost:8501/app/static/abilities/Lesley/Lesley_Master_of_Camouflage.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Lesley.png"
  },
  {
    "id": 35,
    "heroName": "Lesley",
    "skillUrl": "http://localhost:8501/app/static/abilities/Lesley/Lesley_Tactical_Grenade.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Lesley.png"
  },
  {
    "id": 36,
    "heroName": "Lesley",
    "skillUrl": "http://localhost:8501/app/static/abilities/Lesley/Lesley_Ultimate_Snipe.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Lesley.png"
  },
  {
    "id": 37,
    "heroName": "Miya",
    "skillUrl": "http://localhost:8501/app/static/abilities/Miya/Miya_Moon_Arrow.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Miya.png"
  },
  {
    "id": 38,
    "heroName": "Miya",
    "skillUrl": "http://localhost:8501/app/static/abilities/Miya/Miya_Arrow_of_Eclipse.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Miya.png"
  },
  {
    "id": 39,
    "heroName": "Moskov",
    "skillUrl": "http://localhost:8501/app/static/abilities/Moskov/Moskov_Spear_of_Misery.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Moskov.png"
  },
  {
    "id": 40,
    "heroName": "Moskov",
    "skillUrl": "http://localhost:8501/app/static/abilities/Moskov/Moskov_Spear_of_Destruction.png",
    "heroUrl": "http://localhost:8501/app/static/heroes/Moskov.png"
  }
]
    
            
  image_component_streamlit(data=heroes, styles=None)