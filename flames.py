import streamlit as st
st.title("flames game")
a=list(st.text_input("enter first name").lower())
b=list(st.text_input("enter second name").lower())
for i in a.copy():
    if i in b:
        b.remove(i)
        a.remove(i)
    n=len(a+b)
    print(a,b,n)
    s="flames"
    while(len(s)!=1):
        i=n%len(s)-1
        if i==-1:
            s=s[:len(s)-1]
        else:
            s=s[i+1:]+s[:i] 
    d = {'f':'friends',
         'l':'love',
         'a':'affection',
         'm':'marriage',
         'e':'enemies',
         's':'siblings'}
    
if st.button("submit"):
    st.success(d[s])
    print(s)