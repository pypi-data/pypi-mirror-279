import{V as N,W as Ue,X as Z,Y as B,r as c,Z as ye,_ as ne,a0 as ae,a1 as Je,a2 as X,a3 as Xe,a4 as re,a5 as V,a6 as oe,a7 as Se,a8 as Ve,a9 as Ye,j as t,aa as Le,ab as qe,A as ze,t as ee,B as K,ac as Ge,I as P,ad as H,ae as $,h as R,af as F,ag as Qe,ah as q,ai as $e,aj as te,ak as Ze,al as Be,am as et,an as W,ao as xe,u as tt,n as S,ap as U,S as je,aq as be,ar as st,as as nt,at,y as rt}from"./index-f9c70843.js";import{u as z,S as Re,a as ot,b as it,c as lt,d as ve,P as ct}from"./index-b4735d74.js";import{C as dt,I as ut}from"./index-2cf85b82.js";import{u as G}from"./shortcuts-faa601b8.js";import{S as se}from"./tabs-d59cdba9.js";import{H as pt}from"./index-e5253f5c.js";import{I as ht}from"./input-ae70f3cc.js";import{E as ft}from"./index-49516451.js";import"./index-ec47a6a3.js";import"./popover-6c4eec5c.js";import"./textarea-2b2c5564.js";import"./index-0665146f.js";import"./index-d8909728.js";import"./index-21d0a8f9.js";import"./index-de73f900.js";import"./index-6a592cdd.js";import"./index-54d69b5b.js";import"./addNewVariableButton-cc3cadb4.js";import"./index-fadcf4d5.js";import"./index-879843fd.js";import"./checkbox-5461a929.js";import"./table-ef59afbe.js";var ke;let Fe=(ke=N.useId)!=null?ke:function(){let e=Ue(),[s,n]=N.useState(e?()=>Z.nextId():null);return B(()=>{s===null&&n(Z.nextId())},[s]),s!=null?""+s:void 0};function mt(e){return Z.isServer?null:e instanceof Node?e.ownerDocument:e!=null&&e.hasOwnProperty("current")&&e.current instanceof Node?e.current.ownerDocument:document}function we(e){var s;if(e.type)return e.type;let n=(s=e.as)!=null?s:"button";if(typeof n=="string"&&n.toLowerCase()==="button")return"button"}function gt(e,s){let[n,l]=c.useState(()=>we(e));return B(()=>{l(we(e))},[e.type,e.as]),B(()=>{n||s.current&&s.current instanceof HTMLButtonElement&&!s.current.hasAttribute("type")&&l("button")},[n,s]),n}function yt(e){let s=e.parentElement,n=null;for(;s&&!(s instanceof HTMLFieldSetElement);)s instanceof HTMLLegendElement&&(n=s),s=s.parentElement;let l=(s==null?void 0:s.getAttribute("disabled"))==="";return l&&xt(n)?!1:l}function xt(e){if(!e)return!1;let s=e.previousElementSibling;for(;s!==null;){if(s instanceof HTMLLegendElement)return!1;s=s.previousElementSibling}return!0}var L=(e=>(e.Space=" ",e.Enter="Enter",e.Escape="Escape",e.Backspace="Backspace",e.Delete="Delete",e.ArrowLeft="ArrowLeft",e.ArrowUp="ArrowUp",e.ArrowRight="ArrowRight",e.ArrowDown="ArrowDown",e.Home="Home",e.End="End",e.PageUp="PageUp",e.PageDown="PageDown",e.Tab="Tab",e))(L||{}),_e;let jt=(_e=N.startTransition)!=null?_e:function(e){e()};var bt=(e=>(e[e.Open=0]="Open",e[e.Closed=1]="Closed",e))(bt||{}),vt=(e=>(e[e.ToggleDisclosure=0]="ToggleDisclosure",e[e.CloseDisclosure=1]="CloseDisclosure",e[e.SetButtonId=2]="SetButtonId",e[e.SetPanelId=3]="SetPanelId",e[e.LinkPanel=4]="LinkPanel",e[e.UnlinkPanel=5]="UnlinkPanel",e))(vt||{});let kt={0:e=>({...e,disclosureState:re(e.disclosureState,{0:1,1:0})}),1:e=>e.disclosureState===1?e:{...e,disclosureState:1},4(e){return e.linkedPanel===!0?e:{...e,linkedPanel:!0}},5(e){return e.linkedPanel===!1?e:{...e,linkedPanel:!1}},2(e,s){return e.buttonId===s.buttonId?e:{...e,buttonId:s.buttonId}},3(e,s){return e.panelId===s.panelId?e:{...e,panelId:s.panelId}}},ie=c.createContext(null);ie.displayName="DisclosureContext";function le(e){let s=c.useContext(ie);if(s===null){let n=new Error(`<${e} /> is missing a parent <Disclosure /> component.`);throw Error.captureStackTrace&&Error.captureStackTrace(n,le),n}return s}let ce=c.createContext(null);ce.displayName="DisclosureAPIContext";function Me(e){let s=c.useContext(ce);if(s===null){let n=new Error(`<${e} /> is missing a parent <Disclosure /> component.`);throw Error.captureStackTrace&&Error.captureStackTrace(n,Me),n}return s}let de=c.createContext(null);de.displayName="DisclosurePanelContext";function wt(){return c.useContext(de)}function _t(e,s){return re(s.type,kt,e,s)}let Ct=c.Fragment;function Tt(e,s){let{defaultOpen:n=!1,...l}=e,p=c.useRef(null),o=ae(s,Je(a=>{p.current=a},e.as===void 0||e.as===c.Fragment)),d=c.useRef(null),m=c.useRef(null),h=c.useReducer(_t,{disclosureState:n?0:1,linkedPanel:!1,buttonRef:m,panelRef:d,buttonId:null,panelId:null}),[{disclosureState:u,buttonId:x},g]=h,j=X(a=>{g({type:1});let f=mt(p);if(!f||!x)return;let r=(()=>a?a instanceof HTMLElement?a:a.current instanceof HTMLElement?a.current:f.getElementById(x):f.getElementById(x))();r==null||r.focus()}),C=c.useMemo(()=>({close:j}),[j]),v=c.useMemo(()=>({open:u===0,close:j}),[u,j]),w={ref:o};return N.createElement(ie.Provider,{value:h},N.createElement(ce.Provider,{value:C},N.createElement(Xe,{value:re(u,{0:V.Open,1:V.Closed})},oe({ourProps:w,theirProps:l,slot:v,defaultTag:Ct,name:"Disclosure"}))))}let Et="button";function Ot(e,s){let n=Fe(),{id:l=`headlessui-disclosure-button-${n}`,...p}=e,[o,d]=le("Disclosure.Button"),m=wt(),h=m===null?!1:m===o.panelId,u=c.useRef(null),x=ae(u,s,h?null:o.buttonRef),g=Se();c.useEffect(()=>{if(!h)return d({type:2,buttonId:l}),()=>{d({type:2,buttonId:null})}},[l,d,h]);let j=X(r=>{var i;if(h){if(o.disclosureState===1)return;switch(r.key){case L.Space:case L.Enter:r.preventDefault(),r.stopPropagation(),d({type:0}),(i=o.buttonRef.current)==null||i.focus();break}}else switch(r.key){case L.Space:case L.Enter:r.preventDefault(),r.stopPropagation(),d({type:0});break}}),C=X(r=>{switch(r.key){case L.Space:r.preventDefault();break}}),v=X(r=>{var i;yt(r.currentTarget)||e.disabled||(h?(d({type:0}),(i=o.buttonRef.current)==null||i.focus()):d({type:0}))}),w=c.useMemo(()=>({open:o.disclosureState===0}),[o]),a=gt(e,u),f=h?{ref:x,type:a,onKeyDown:j,onClick:v}:{ref:x,id:l,type:a,"aria-expanded":o.disclosureState===0,"aria-controls":o.linkedPanel?o.panelId:void 0,onKeyDown:j,onKeyUp:C,onClick:v};return oe({mergeRefs:g,ourProps:f,theirProps:p,slot:w,defaultTag:Et,name:"Disclosure.Button"})}let Pt="div",Dt=ye.RenderStrategy|ye.Static;function It(e,s){let n=Fe(),{id:l=`headlessui-disclosure-panel-${n}`,...p}=e,[o,d]=le("Disclosure.Panel"),{close:m}=Me("Disclosure.Panel"),h=Se(),u=ae(s,o.panelRef,v=>{jt(()=>d({type:v?4:5}))});c.useEffect(()=>(d({type:3,panelId:l}),()=>{d({type:3,panelId:null})}),[l,d]);let x=Ve(),g=(()=>x!==null?(x&V.Open)===V.Open:o.disclosureState===0)(),j=c.useMemo(()=>({open:o.disclosureState===0,close:m}),[o,m]),C={ref:u,id:l};return N.createElement(de.Provider,{value:o.panelId},oe({mergeRefs:h,ourProps:C,theirProps:p,slot:j,defaultTag:Pt,features:Dt,visible:g,name:"Disclosure.Panel"}))}let At=ne(Tt),Nt=ne(Ot),St=ne(It),M=Object.assign(At,{Button:Nt,Panel:St});const J=Ye((e,s)=>({tweak:[],setTweak:n=>e({tweak:n}),tweaksList:[],setTweaksList:n=>e({tweaksList:n})}));function Lt(e){return t.jsx("div",{className:"w-[200px]",children:t.jsx("span",{children:e!=null&&e!=""?e:"None"})})}function Ce(e){return e.data.nodes.reduce((s,n)=>(s[n.data.id]={},s),{})}const $t=(e,s)=>e.data.node.template[s]&&s.charAt(0)!=="_"&&e.data.node.template[s].show&&Le.has(e.data.node.template[s].type)&&s!=="code",Rt=(e,s)=>(typeof e=="string"&&s.type==="float"&&(e=parseFloat(e)),typeof e=="string"&&s.type==="int"&&(e=parseInt(e)),s.list===!0&&Array.isArray(e)&&(e=e==null?void 0:e.filter(n=>n!=="")),s.type==="dict"&&Array.isArray(e)&&(e=qe(e)),s.type==="NestedDict"&&(e=JSON.stringify(e)),e);function Te(e,s,n,l){const p=n[0];return`curl -X POST \\
    "${window.location.protocol}//${window.location.host}/api/v1/run/${l||e}?stream=false" \\
    -H 'Content-Type: application/json'\\${s?"":`
  -H 'x-api-key: <your api key>'\\`}
    -d '{"input_value": "message",
    "output_type": "chat",
    "input_type": "chat",
    "tweaks": ${JSON.stringify(p,null,2)}}'
    `}function Ft(e,s,n){return`curl -X POST \\
  "${window.location.protocol}//${window.location.host}/api/v1/webhook/${n||e}" \\
  -H 'Content-Type: application/json'\\${s?"":`
  -H 'x-api-key: <your api key>'\\`}
  -d '{"any": "data"}'
  `}const Mt=e=>{let s=[];return e.data.nodes.forEach(l=>{l.data.node.template&&Object.keys(l.data.node.template).filter(p=>{var o,d;return p.charAt(0)!=="_"&&((o=l.data.node.template[p])==null?void 0:o.show)&&Le.has((d=l.data.node.template[p])==null?void 0:d.type)}).map((p,o)=>{s.push(l.id)})}),s.filter((l,p,o)=>o.indexOf(l)===p)};function Ee(e,s,n,l){let p="{}";if(n&&n.length>0){const o=n[0];if(!o)throw new Error("expected tweaks");p=JSON.stringify(o,null,2).replace(/true/g,"True").replace(/false/g,"False")}return`import argparse
import json
from argparse import RawTextHelpFormatter
import requests
from typing import Optional
import warnings
try:
    from langflow.load import upload_file
except ImportError:
    warnings.warn("Langflow provides a function to help you upload files to the flow. Please install langflow to use it.")
    upload_file = None

BASE_API_URL = "${window.location.protocol}//${window.location.host}/api/v1/run"
FLOW_ID = "${e}"
ENDPOINT = "${l||""}" ${l?"# The endpoint name of the flow":"# You can set a specific endpoint name in the flow settings"}

# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = ${p}

def run_flow(message: str,
  endpoint: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  api_key: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if api_key:
        headers = {"x-api-key": api_key}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="""Run a flow with a given message and optional tweaks.
Run it like: python <your file>.py "your message here" --endpoint "your_endpoint" --tweaks '{"key": "value"}'""",
        formatter_class=RawTextHelpFormatter)
    parser.add_argument("message", type=str, help="The message to send to the flow")
    parser.add_argument("--endpoint", type=str, default=ENDPOINT or FLOW_ID, help="The ID or the endpoint name of the flow")
    parser.add_argument("--tweaks", type=str, help="JSON string representing the tweaks to customize the flow", default=json.dumps(TWEAKS))
    parser.add_argument("--api_key", type=str, help="API key for authentication", default=None)
    parser.add_argument("--output_type", type=str, default="chat", help="The output type")
    parser.add_argument("--input_type", type=str, default="chat", help="The input type")
    parser.add_argument("--upload_file", type=str, help="Path to the file to upload", default=None)
    parser.add_argument("--components", type=str, help="Components to upload the file to", default=None)

    args = parser.parse_args()
    try:
      tweaks = json.loads(args.tweaks)
    except json.JSONDecodeError:
      raise ValueError("Invalid tweaks JSON string")

    if args.upload_file:
        if not upload_file:
            raise ImportError("Langflow is not installed. Please install it to use the upload_file function.")
        elif not args.components:
            raise ValueError("You need to provide the components to upload the file to.")
        tweaks = upload_file(file_path=args.upload_file, host=BASE_API_URL, flow_id=ENDPOINT, components=args.components, tweaks=tweaks)

    response = run_flow(
        message=args.message,
        endpoint=args.endpoint,
        output_type=args.output_type,
        input_type=args.input_type,
        tweaks=tweaks,
        api_key=args.api_key
    )

    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main()
`}function Oe(e,s){let n="{}";if(s&&s.length>0){const l=s[0];if(!l)throw new Error("expected tweaks");n=JSON.stringify(l,null,2).replace(/true/g,"True").replace(/false/g,"False")}return`from langflow.load import run_flow_from_json
TWEAKS = ${n}

result = run_flow_from_json(flow="${e}.json",
                            input_value="message",
                            fallback_to_env_vars=True, # False by default
                            tweaks=TWEAKS)`}const Wt=(e,s,n,l)=>{let p=e??"";if(l.length>0)for(const o of l)Object.keys(o).forEach(d=>{const m=o[d];d==s.id&&Object.keys(m).forEach(h=>{h==n.name&&(p=m[h])})});else return e??"";return p};function Pe(e,s,n){return`<script src="https://cdn.jsdelivr.net/gh/langflow-ai/langflow-embedded-chat@1.0_alpha/dist/build/static/js/bundle.min.js"><\/script>

  <langflow-chat
    window_title="${s}"
    flow_id="${e}"
    host_url="http://localhost:7860"${n?"":`
    api_key="..."`}

  ></langflow-chat>`}function Q(e,s=!1,n=!1){const l=[{name:"Run cURL",mode:"bash",image:"https://curl.se/logo/curl-symbol-transparent.png",language:"sh",code:e[0]},{name:"Python API",mode:"python",image:"https://images.squarespace-cdn.com/content/v1/5df3d8c5d2be5962e4f87890/1628015119369-OY4TV3XJJ53ECO0W2OLQ/Python+API+Training+Logo.png?format=1000w",language:"py",code:e[2]},{name:"Python Code",mode:"python",image:"https://cdn-icons-png.flaticon.com/512/5968/5968350.png",language:"py",code:e[3]},{name:"Chat Widget HTML",description:"Insert this code anywhere in your &lt;body&gt; tag. To use with react and other libs, check our <a class='link-color' href='https://langflow.org/guidelines/widget'>documentation</a>.",mode:"html",image:"https://cdn-icons-png.flaticon.com/512/5968/5968350.png",language:"html",code:e[4]}];return s&&l.splice(1,0,{name:"Webhook cURL",mode:"bash",image:"https://curl.se/logo/curl-symbol-transparent.png",language:"sh",code:e[1]}),n&&l.push({name:"Tweaks",mode:"python",image:"https://cdn-icons-png.flaticon.com/512/5968/5968350.png",language:"py",code:e[5]}),l}const Ht=c.forwardRef(({flow:e,children:s,open:n,setOpen:l},p)=>{const o=J(b=>b.tweak),d=J(b=>b.setTweak),m=J(b=>b.setTweaksList),h=J(b=>b.tweaksList),[u,x]=c.useState(!1),{autoLogin:g}=c.useContext(ze),[j,C]=l!==void 0&&n!==void 0?[n,l]:c.useState(!1),[v,w]=c.useState("0"),a=Ee(e==null?void 0:e.id,g,o,e==null?void 0:e.endpoint_name),f=Te(e==null?void 0:e.id,g,o,e==null?void 0:e.endpoint_name),r=Ft(e==null?void 0:e.id,g,e==null?void 0:e.endpoint_name),i=Oe(e==null?void 0:e.name,o),_=Pe(e==null?void 0:e.id,e==null?void 0:e.name,g),k=e.webhook,y=Ce(e),T=[f,r,a,i,_,i],[D,ue]=c.useState(Q(T,k)),We=e&&e.data&&e.data.nodes&&o&&(o==null?void 0:o.length)>0&&u===!0,pe=()=>{const b=[],O=Ce(e);b.push(O),d(b),fe(b)};c.useEffect(()=>{e.data.nodes.length==0?(d([]),m([])):pe(),He(),Object.keys(y).length>0&&w("0"),ue(Q(T,k,!0))},[e.data.nodes,j]),c.useEffect(()=>{We?e.data.nodes.forEach(O=>{const I=O.id,A=O.data.node.template;Object.keys(A).forEach(E=>{$t(O,E)&&he(I,O.data.node.template[E].value,O.data.node.template[E])})}):pe()},[u]);const He=()=>{m(Mt(e))};async function he(b,O,I){O=Rt(O,I);const A=o.find(E=>E.hasOwnProperty(b));if(A)A[b][I.name]=O,A[b][I.name]==I.value&&o.forEach(E=>{var me;if(E[b]&&((me=Object.keys(E[b]))==null?void 0:me.length)===0){const Ke=o.filter(ge=>{const Y=ge[Object.keys(ge)[0]].prop;return Y!=null&&Y!==""});d(Ke)}});else{const E={[b]:{[I.name]:O}};o.push(E)}if(o&&o.length>0){const E=ee.cloneDeep(o);fe(E),d(E)}}const fe=b=>{const O=Ee(e==null?void 0:e.id,g,b),I=Te(e==null?void 0:e.id,g,b,e==null?void 0:e.endpoint_name),A=Oe(e==null?void 0:e.name,b),E=Pe(e==null?void 0:e.id,e==null?void 0:e.name,g);D&&(D==null?void 0:D.length)>0&&(D[0].code=I,D[1].code=O,D[2].code=A,D[3].code=E)};return t.jsxs(K,{open:j,setOpen:C,children:[t.jsx(K.Trigger,{asChild:!0,children:s}),t.jsxs(K.Header,{description:Ge,children:[t.jsx("span",{className:"pr-2",children:"API"}),t.jsx(P,{name:"Code2",className:"h-6 w-6 pl-1 text-gray-800 dark:text-white","aria-hidden":"true"})]}),t.jsx(K.Content,{overflowHidden:!0,children:t.jsx(dt,{flow:e,tabs:D,activeTab:v,setActiveTab:w,tweaks:{tweak:o,tweaksList:h,buildContent:Lt,buildTweakObject:he,getValue:Wt},activeTweaks:u,setActiveTweaks:x,allowExport:!0})})]})}),Kt=Ht;function Ut(){const[s,n]=c.useState(!1),[l,p]=c.useState(!1),[o,d]=c.useState(!1);function m(i){q()&&!l||p(_=>!_)}function h(i){q()&&!s||H.getState().hasIO&&n(_=>!_)}function u(i){q()&&!o||d(_=>!_)}const x=G(i=>i.open),g=G(i=>i.api),j=G(i=>i.flow);z(x,h,{preventDefault:!0}),z(g,m,{preventDefault:!0}),z(j,u,{preventDefault:!0});const C=H(i=>i.hasIO),v=$(i=>i.hasStore),w=$(i=>i.validApiKey),a=$(i=>i.hasApiKey),f=R(i=>i.currentFlow);c.useRef();const r=c.useMemo(()=>t.jsx(Re,{is_component:!1,component:f,disabled:!a||!w||!v,open:o,setOpen:d,children:t.jsxs("button",{disabled:!a||!w||!v,className:F("relative inline-flex h-full w-full items-center justify-center gap-[4px] bg-muted px-5 py-3 text-sm font-semibold text-foreground transition-all duration-150 ease-in-out hover:bg-background hover:bg-hover ",!a||!w||!v?" button-disable text-muted-foreground  ":""),children:[t.jsx(P,{name:"Share3",className:F("-m-0.5 -ml-1 h-6 w-6",!a||!w||!v?"extra-side-bar-save-disable":"")}),"Share"]})}),[a,w,f,v,o,d]);return t.jsx(t.Fragment,{children:t.jsx(Qe,{show:!0,appear:!0,enter:"transition ease-out duration-300",enterFrom:"translate-y-96",enterTo:"translate-y-0",leave:"transition ease-in duration-300",leaveFrom:"translate-y-0",leaveTo:"translate-y-96",children:t.jsx("div",{className:"shadow-round-btn-shadow hover:shadow-round-btn-shadow message-button-position flex items-center justify-center gap-7 rounded-sm  border bg-muted shadow-md transition-all",children:t.jsxs("div",{className:"flex",children:[t.jsx("div",{className:"flex h-full w-full  gap-1 rounded-sm transition-all",children:C?t.jsx(ut,{open:s,setOpen:n,disable:!C,children:t.jsxs("div",{className:"relative inline-flex w-full items-center justify-center   gap-1 px-5 py-3 text-sm font-semibold transition-all duration-500 ease-in-out hover:bg-hover",children:[t.jsx(P,{name:"BotMessageSquareIcon",className:" h-5 w-5 transition-all"}),"Playground"]})}):t.jsxs("div",{className:"relative inline-flex w-full cursor-not-allowed items-center justify-center gap-1 px-5 py-3 text-sm font-semibold text-muted-foreground transition-all duration-150 ease-in-out ease-in-out",children:[t.jsx(P,{name:"BotMessageSquareIcon",className:" h-5 w-5 transition-all"}),"Playground"]})}),t.jsx("div",{children:t.jsx(se,{orientation:"vertical"})}),t.jsx("div",{className:"flex cursor-pointer items-center gap-2",children:f&&f.data&&t.jsx(Kt,{flow:f,open:l,setOpen:p,children:t.jsxs("div",{className:F("relative inline-flex w-full items-center justify-center gap-1 px-5 py-3 text-sm font-semibold text-foreground transition-all duration-150 ease-in-out hover:bg-hover"),children:[t.jsx(P,{name:"Code2",className:" h-5 w-5"}),"API"]})})}),t.jsx("div",{children:t.jsx(se,{orientation:"vertical"})}),t.jsx("div",{className:"flex items-center gap-2",children:t.jsx("div",{className:`side-bar-button ${!a||!w||!v?" cursor-not-allowed":" cursor-pointer"}`,children:r})})]})})})})}function De({button:{title:e,Icon:s,buttons:n=[]},isChild:l=!0,children:p,openDisc:o}){return t.jsx(M,{as:"div",defaultOpen:o,children:({open:d})=>t.jsxs(t.Fragment,{children:[t.jsx("div",{children:t.jsxs(M.Button,{className:l?"components-disclosure-arrangement-child":"components-disclosure-arrangement","data-testid":`disclosure-${e.toLocaleLowerCase()}`,children:[t.jsxs("div",{className:"flex gap-4"+(l?" pl-2":""),children:[t.jsx(s,{strokeWidth:1.5,size:22,className:"text-primary"}),t.jsx("span",{className:"components-disclosure-title",children:e})]}),t.jsxs("div",{className:"components-disclosure-div",children:[n.map((m,h)=>t.jsx("button",{onClick:m.onClick,children:m.Icon},h)),t.jsx("div",{children:t.jsx(P,{name:"ChevronRight",className:`${d||o?"rotate-90 transform":""} h-4 w-4 text-foreground`})})]})]})}),t.jsx(M.Panel,{as:"div",children:p})]})},e)}function Jt({button:{title:e,Icon:s,buttons:n=[]},children:l,openDisc:p,testId:o}){return t.jsx(M,{as:"div",defaultOpen:p,children:({open:d})=>t.jsxs(t.Fragment,{children:[t.jsx("div",{children:t.jsxs(M.Button,{className:"parent-disclosure-arrangement","data-testid":o,children:[t.jsx("div",{className:"flex gap-4",children:t.jsx("span",{className:"parent-disclosure-title ",children:e})}),t.jsxs("div",{className:"components-disclosure-div",children:[n.map((m,h)=>t.jsx("button",{onClick:m.onClick,children:m.Icon},h)),t.jsx("div",{children:t.jsx(P,{name:"ChevronsUpDownIcon",className:" h-4 w-4 text-foreground"})})]})]})}),t.jsx(M.Panel,{as:"div",children:l})]})},e)}const Xt=c.forwardRef(({sectionName:e,display_name:s,itemName:n,error:l,color:p,onDragStart:o,apiClass:d,official:m},h)=>{const[u,x]=c.useState(!1),g=R(r=>r.deleteComponent),j=$e(r=>r.version),[C,v]=c.useState({x:0,y:0}),w=c.useRef(null),a=r=>{var i;if(!u){const _=((i=w.current)==null?void 0:i.getBoundingClientRect())??{left:0,top:0};v({x:r.clientX-_.left,y:r.clientY-_.top})}};function f(r){switch(r){case"share":break;case"download":const i=te(n);Ze(Be({id:et(i),type:i,node:d},j));break;case"delete":g(s);break}}return t.jsx(ot,{onValueChange:f,onOpenChange:r=>x(r),open:u,children:t.jsx("div",{onPointerDown:a,onContextMenuCapture:r=>{r.preventDefault(),x(!0)},"data-tooltip-id":n,children:t.jsx("div",{draggable:!l,className:"side-bar-components-border bg-background"+(l?" cursor-not-allowed select-none":""),style:{borderLeftColor:p},onDragStart:o,onDragEnd:()=>{document.body.removeChild(document.getElementsByClassName("cursor-grabbing")[0])},children:t.jsxs("div",{"data-testid":e+s,id:e+s,className:"side-bar-components-div-form",children:[t.jsx("span",{className:"side-bar-components-text",children:s}),t.jsxs("div",{ref:w,children:[t.jsx(P,{name:"Menu",className:"side-bar-components-icon "}),t.jsx(it,{}),t.jsxs(lt,{position:"popper",side:"bottom",sideOffset:-25,style:{position:"absolute",left:C.x,top:C.y},children:[t.jsxs(ve,{value:"download",children:[t.jsxs("div",{className:"flex",children:[t.jsx(P,{name:"Download",className:"relative top-0.5 mr-2 h-4 w-4"})," ","Download"," "]})," "]}),!m&&t.jsxs(ve,{value:"delete",children:[t.jsxs("div",{className:"flex",children:[t.jsx(P,{name:"Trash2",className:"relative top-0.5 mr-2 h-4 w-4"})," ","Delete"," "]})," "]})]})]})]})})},n)},n)}),Ie=Xt;function Ae(e,s){const n=W.indexOf(e.toLowerCase()),l=W.indexOf(s.toLowerCase());return n!==-1&&l!==-1?n-l:n!==-1?-1:l!==-1?1:e.localeCompare(s)}function Ne(e,s){const n=/(.+) \((\w+)\)/,l=e.match(n),p=s.match(n);if(l&&p){const o=l[1],d=p[1];if(o!==d)return o.localeCompare(d);const m=parseInt(l[2]),h=parseInt(p[2]);return m-h}else return e.localeCompare(s)}function Vt(){const e=xe(a=>a.data),s=xe(a=>a.templates),n=H(a=>a.getFilterEdge),l=H(a=>a.setFilterEdge),p=R(a=>a.currentFlow),o=$(a=>a.hasStore),d=$(a=>a.hasApiKey),m=$(a=>a.validApiKey),h=tt(a=>a.setErrorData),[u,x]=c.useState(e),[g,j]=c.useState("");function C(a,f){var r=a.currentTarget.cloneNode(!0);r.style.position="absolute",r.style.top="-500px",r.style.right="-500px",r.classList.add("cursor-grabbing"),document.body.appendChild(r),a.dataTransfer.setDragImage(r,0,0),a.dataTransfer.setData("nodedata",JSON.stringify(f))}function v(a){if(a===""){x(e);return}x(f=>{let r={};return Object.keys(e).forEach((i,_)=>{r[i]={},Object.keys(e[i]).filter(y=>{var T;return y.toLowerCase().includes(a.toLowerCase())||((T=e[i][y].display_name)==null?void 0:T.toLowerCase().includes(a.toLowerCase()))}).forEach(y=>{r[i][y]=e[i][y]})}),r})}c.useEffect(()=>{let a=[];Object.keys(s).forEach(f=>{s[f].error&&a.push(f)}),a.length>0&&h({title:" Components with errors: ",list:a})},[]);function w(){(!g&&g===""||g==="search")&&(x(e),l([]),j(""))}return c.useEffect(()=>{n.length!==0&&j(""),n.length===0&&g===""&&(j(""),x(e))},[n,e]),c.useEffect(()=>{v(g)},[e]),c.useEffect(()=>{(n==null?void 0:n.length)>0&&x(a=>{let f=ee.cloneDeep(e),r={};return Object.keys(f).forEach((i,_)=>{if(r[i]={},n.some(k=>k.family===i)){r[i]=f[i];const k=n.filter(y=>y.family===i).pop().type.split(",");for(let y=0;y<k.length;y++)k[y]=k[y].trimStart();if(k.some(y=>y!=="")){let y=Object.keys(f[i]).filter(T=>k.includes(T));Object.keys(f[i]).forEach(T=>{y.includes(T)||delete r[i][T]})}}}),j(""),r})},[n]),c.useEffect(()=>{(n==null?void 0:n.length)>0&&x(a=>{let f=ee.cloneDeep(e),r={};return Object.keys(f).forEach((i,_)=>{if(r[i]={},n.some(k=>k.family===i)){r[i]=f[i];const k=n.filter(y=>y.family===i).pop().type.split(",");for(let y=0;y<k.length;y++)k[y]=k[y].trimStart();if(k.some(y=>y!=="")){let y=Object.keys(f[i]).filter(T=>k.includes(T));Object.keys(f[i]).forEach(T=>{y.includes(T)||delete r[i][T]})}}}),j(""),r})},[n,e]),c.useMemo(()=>t.jsx(Re,{is_component:!1,component:p,disabled:!d||!m||!o,children:t.jsxs("button",{disabled:!d||!m||!o,className:F("extra-side-bar-buttons gap-[4px] text-sm font-semibold",!d||!m||!o?"button-disable  cursor-default text-muted-foreground":""),children:[t.jsx(P,{name:"Share3",className:F("-m-0.5 -ml-1 h-6 w-6",!d||!m||!o?"extra-side-bar-save-disable":"")}),"Share"]})}),[d,m,p,o]),c.useMemo(()=>t.jsx(ft,{children:t.jsx("button",{className:F("extra-side-bar-buttons"),children:t.jsx(P,{name:"FileDown",className:"side-bar-button-size"})})}),[]),c.useMemo(()=>a=>{if(S[a])return t.jsx(P,{name:a,strokeWidth:1.5,className:"w-[22px] text-primary"})},[]),t.jsxs("div",{className:"side-bar-arrangement",children:[t.jsxs("div",{className:"side-bar-search-div-placement",children:[t.jsx(ht,{onFocusCapture:()=>w(),value:g,type:"text",name:"search",id:"search",placeholder:"Search",className:"nopan nodelete nodrag noundo nocopy input-search",onChange:a=>{v(a.target.value),j(a.target.value)}}),t.jsx("div",{className:"search-icon ",onClick:()=>{g&&(x(e),j(""))},children:t.jsx(P,{name:g?"X":"Search",className:`h-5 w-5 stroke-[1.5] text-primary ${g?"cursor-pointer":"cursor-default"}`,"aria-hidden":"true"})})]}),t.jsx(se,{}),t.jsxs("div",{className:"side-bar-components-div-arrangement",children:[t.jsx("div",{className:"parent-disclosure-arrangement",children:t.jsx("div",{className:"flex items-center gap-4 align-middle",children:t.jsx("span",{className:"parent-disclosure-title",children:"Basic Components"})})}),Object.keys(u).sort(Ae).filter(a=>W.includes(a)).map((a,f)=>Object.keys(u[a]).length>0?t.jsx(t.Fragment,{children:t.jsx(De,{openDisc:n.length!==0||g.length!==0,isChild:!1,button:{title:U[a]??U.unknown,Icon:S[a]??S.unknown},children:t.jsx("div",{className:"side-bar-components-gap",children:Object.keys(u[a]).sort((r,i)=>Ne(u[a][r].display_name,u[a][i].display_name)).map((r,i)=>t.jsx(je,{content:u[a][r].display_name,side:"right",children:t.jsx(Ie,{sectionName:a,apiClass:u[a][r],onDragStart:_=>C(_,{type:te(r),node:u[a][r]}),color:be[a],itemName:r,error:!!u[a][r].error,display_name:u[a][r].display_name,official:u[a][r].official!==!1},i+r)},i))})},f+g+JSON.stringify(n))}):t.jsx("div",{},f))," ",t.jsx(Jt,{openDisc:!1,button:{title:"Advanced",Icon:S.unknown},testId:"extended-disclosure",children:Object.keys(u).sort(Ae).filter(a=>!W.includes(a)).map((a,f)=>Object.keys(u[a]).length>0?t.jsxs(t.Fragment,{children:[t.jsx(De,{isChild:!1,openDisc:n.length!==0||g.length!==0,button:{title:U[a]??U.unknown,Icon:S[a]??S.unknown},children:t.jsx("div",{className:"side-bar-components-gap",children:Object.keys(u[a]).sort((r,i)=>Ne(u[a][r].display_name,u[a][i].display_name)).map((r,i)=>t.jsx(je,{content:u[a][r].display_name,side:"right",children:t.jsx(Ie,{sectionName:a,apiClass:u[a][r],onDragStart:_=>C(_,{type:te(r),node:u[a][r]}),color:be[a],itemName:r,error:!!u[a][r].error,display_name:u[a][r].display_name,official:u[a][r].official!==!1},i)},i))})},f+g+JSON.stringify(n)),f===Object.keys(u).length-W.length+1&&t.jsx(t.Fragment,{children:t.jsxs("a",{target:"_blank",href:"https://langflow.store",className:"components-disclosure-arrangement",children:[t.jsxs("div",{className:"flex gap-4",children:[t.jsx(st,{strokeWidth:1.5,className:"w-[22px] text-primary"}),t.jsx("span",{className:"components-disclosure-title",children:"Discover More"})]}),t.jsx("div",{className:"components-disclosure-div",children:t.jsx("div",{children:t.jsx(nt,{className:"h-4 w-4 text-foreground"})})})]})})]}):t.jsx("div",{},f))},"Advanced")]})]})}function ms({view:e}){const s=R(h=>h.setCurrentFlowId),n=$e(h=>h.version),l=H(h=>h.setOnFlowPage),p=R(h=>h.currentFlow),{id:o}=at(),d=rt(),m=R(h=>h.flows);return c.useEffect(()=>{if(!m.some(u=>u.id===o)){d("/all");return}return s(o),l(!0),()=>{l(!1)}},[o]),t.jsxs(t.Fragment,{children:[t.jsx(pt,{}),t.jsxs("div",{className:"flow-page-positioning",children:[p&&t.jsxs("div",{className:"flex h-full overflow-hidden",children:[!e&&t.jsx(Vt,{}),t.jsxs("main",{className:"flex flex-1",children:[t.jsx("div",{className:"h-full w-full",children:t.jsx(ct,{flow:p})}),!e&&t.jsx(Ut,{})]})]}),t.jsxs("a",{target:"_blank",href:"https://medium.com/logspace/langflow-datastax-better-together-1b7462cebc4d",className:"langflow-page-icon",children:[n&&t.jsx("div",{className:"mt-1",children:"Langflow 🤝 DataStax"}),t.jsxs("div",{className:n?"mt-2":"mt-1",children:["⛓️ v",n]})]})]})]})}export{ms as default};
