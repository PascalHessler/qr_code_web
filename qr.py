import streamlit as st
from osmnx.geocoder import geocode
from segno import helpers

st.write("""
# Generate GEO QR Codes
""")

import streamlit as st

tab1, tab2 = st.tabs(["Address", "Lat long"])


with tab1:
    with st.form(key='my_form'):
        address = st.text_input("Location address", help="Enter the address you want to create a qr code for")
        col1, col2 = st.columns(2)
        with col1:
            bg_color = st.color_picker('Background Color', value='#FFFFFF', help="Background color of the qr code in hex format or name")
            scale = st.slider('Scale of picture', min_value=1, max_value=50, value=30,
                              help="Higher values result in a higher resolution image")
        with col2:
            fg_color = st.color_picker('QR Color', value='#000000',
                                     help="Color of the qr code itself in hex format or name")
            border = st.slider('Border', min_value=0, max_value=10, value=1,
                               help="Higher values result in a larger border")

        st.form_submit_button('Generate QR Code')
    try:
        if address != "":
            lat, lon = geocode(address)
            st.write(f"Created qr code for {address} at {lat}, {lon}")
            qr_code = helpers.make_geo(lat, lon)
            qr_code.save('geo.png', scale=scale, border=border, light=bg_color, dark=fg_color)

            st.image('geo.png')
    except ValueError as e:
        st.error(str(e))
        st.stop()


with tab2:
    with st.form(key='my_form2'):
        col3, col4 = st.columns(2)



        with col3:
            lat = st.text_input("Latitude", )
            bg_color = st.color_picker('Background Color', value='#FFFFFF', help="Background color of the qr code in hex format or name")
            scale = st.slider('Scale of picture', min_value=1, max_value=50, value=30,
                              help="Higher values result in a higher resolution image")
        with col4:
            long = st.text_input("Longitude", )
            fg_color = st.color_picker('QR Color', value='#000000',
                                     help="Color of the qr code itself in hex format or name")
            border = st.slider('Border', min_value=0, max_value=10, value=1,
                               help="Higher values result in a larger border")

        st.form_submit_button('Generate QR Code')


    try:
        if lat != "" and long != "":

            st.write(f"Created qr code for at {lat}, {lon}")
            qr_code = helpers.make_geo(float(lat), float(lon))
            qr_code.save('geo2.png', scale=scale, border=border, light=bg_color, dark=fg_color)

            st.image('geo2.png')
    except ValueError as e:
        st.error(str(e))
        st.stop()



# svg_string = plt_to_svg(fig)
# html = svg_to_html(svg_string)
# st.write("")