import{r as s,u as G,ao as N,bk as g,j as a,B as r,I as A,dx as O}from"./index-f9c70843.js";import{I as m}from"./index-ec47a6a3.js";import{I as B}from"./input-ae70f3cc.js";import{L as d,T as E}from"./textarea-2b2c5564.js";function k(c){return c.sort((p,o)=>p.localeCompare(o))}function K({children:c,asChild:p}){const[o,x]=s.useState(""),[u,b]=s.useState(""),[h,v]=s.useState("Generic"),[f,j]=s.useState([]),[S,y]=s.useState(!1),C=G(e=>e.setErrorData),w=N(e=>e.ComponentFields),V=new Set(Object.keys(g(e=>e.unavaliableFields))),I=()=>{const e=Array.from(w).filter(t=>!V.has(t));return k(e)},T=g(e=>e.addGlobalVariable);function F(){O({name:o,type:h,value:u,default_fields:f}).then(t=>{const{name:l,id:n,type:i}=t.data;T(l,n,i,f),x(""),b(""),v(""),j([]),y(!1)}).catch(t=>{var n,i;let l=t;C({title:"Error creating variable",list:[((i=(n=l==null?void 0:l.response)==null?void 0:n.data)==null?void 0:i.detail)??"An unexpected error occurred while adding a new variable. Please try again."]})})}return a.jsxs(r,{open:S,setOpen:y,size:"x-small",onSubmit:F,children:[a.jsxs(r.Header,{description:"This variable will be encrypted and will be available for you to use in any of your projects.",children:[a.jsx("span",{className:"pr-2",children:" Create Variable "}),a.jsx(A,{name:"Globe",className:"h-6 w-6 pl-1 text-primary ","aria-hidden":"true"})]}),a.jsx(r.Trigger,{asChild:p,children:c}),a.jsx(r.Content,{children:a.jsxs("div",{className:"flex h-full w-full flex-col gap-4 align-middle",children:[a.jsx(d,{children:"Variable Name"}),a.jsx(B,{value:o,onChange:e=>{x(e.target.value)},placeholder:"Insert a name for the variable..."}),a.jsx(d,{children:"Type (optional)"}),a.jsx(m,{setSelectedOption:e=>{v(e)},selectedOption:h,password:!1,options:["Generic","Credential"],placeholder:"Choose a type for the variable...",id:"type-global-variables"}),a.jsx(d,{children:"Value"}),h==="Credential"?a.jsx(m,{password:!0,value:u,onChange:e=>{b(e)},placeholder:"Insert a value for the variable..."}):a.jsx(E,{value:u,onChange:e=>{b(e.target.value)},placeholder:"Insert a value for the variable...",className:"w-full resize-none custom-scroll"}),a.jsx(d,{children:"Apply To Fields (optional)"}),a.jsx(m,{setSelectedOptions:e=>j(e),selectedOptions:f,options:I(),password:!1,placeholder:"Choose a field for the variable...",id:"apply-to-fields"})]})}),a.jsx(r.Footer,{submit:{label:"Save Variable",dataTestId:"save-variable-btn"}})]})}export{K as A};
