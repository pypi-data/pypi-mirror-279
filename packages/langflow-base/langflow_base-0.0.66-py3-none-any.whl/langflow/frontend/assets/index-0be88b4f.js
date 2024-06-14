import{r as l,z as g,A as N,y as v,u as b,j as e,$ as w,a as i,b as c,c as $,d,g as I,f as o,au as S,D as y,F as C}from"./index-f9c70843.js";import{I as E}from"./index-ec47a6a3.js";import{I as D}from"./input-ae70f3cc.js";import"./popover-6c4eec5c.js";function P(){const[u,m]=l.useState(g),{password:t,username:n}=u,{login:x}=l.useContext(N),f=v(),p=b(a=>a.setErrorData);function r({target:{name:a,value:s}}){m(j=>({...j,[a]:s}))}function h(){const a={username:n.trim(),password:t.trim()};y(a).then(s=>{x(s.access_token),f("/")}).catch(s=>{p({title:C,list:[s.response.data.detail]})})}return e.jsx(w,{onSubmit:a=>{if(t===""){a.preventDefault();return}h(),Object.fromEntries(new FormData(a.currentTarget)),a.preventDefault()},className:"h-full w-full",children:e.jsx("div",{className:"flex h-full w-full flex-col items-center justify-center bg-muted",children:e.jsxs("div",{className:"flex w-72 flex-col items-center justify-center gap-2",children:[e.jsx("span",{className:"mb-4 text-5xl",children:"⛓️"}),e.jsx("span",{className:"mb-6 text-2xl font-semibold text-primary",children:"Sign in to Langflow"}),e.jsx("div",{className:"mb-3 w-full",children:e.jsxs(i,{name:"username",children:[e.jsxs(c,{className:"data-[invalid]:label-invalid",children:["Username ",e.jsx("span",{className:"font-medium text-destructive",children:"*"})]}),e.jsx($,{asChild:!0,children:e.jsx(D,{type:"username",onChange:({target:{value:a}})=>{r({target:{name:"username",value:a}})},value:n,className:"w-full",required:!0,placeholder:"Username"})}),e.jsx(d,{match:"valueMissing",className:"field-invalid",children:"Please enter your username"})]})}),e.jsx("div",{className:"mb-3 w-full",children:e.jsxs(i,{name:"password",children:[e.jsxs(c,{className:"data-[invalid]:label-invalid",children:["Password ",e.jsx("span",{className:"font-medium text-destructive",children:"*"})]}),e.jsx(E,{onChange:a=>{r({target:{name:"password",value:a}})},value:t,isForm:!0,password:!0,required:!0,placeholder:"Password",className:"w-full"}),e.jsx(d,{className:"field-invalid",match:"valueMissing",children:"Please enter your password"})]})}),e.jsx("div",{className:"w-full",children:e.jsx(I,{asChild:!0,children:e.jsx(o,{className:"mr-3 mt-6 w-full",type:"submit",children:"Sign in"})})}),e.jsx("div",{className:"w-full",children:e.jsx(S,{to:"/signup",children:e.jsxs(o,{className:"w-full",variant:"outline",type:"button",children:["Don't have an account? ",e.jsx("b",{children:"Sign Up"})]})})})]})})})}export{P as default};
