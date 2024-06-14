import{bE as O,r as o,bI as g,bL as re,bF as G,cm as ce,bH as E,bJ as I,bG as k,j as w,av as R,bK as se}from"./index-f9c70843.js";import{$ as ie,a as V}from"./index-d8909728.js";const S="rovingFocusGroup.onEntryFocus",de={bubbles:!1,cancelable:!0},N="RovingFocusGroup",[A,L,fe]=ie(N),[be,K]=O(N,[fe]),[ue,le]=be(N),$e=o.forwardRef((e,t)=>o.createElement(A.Provider,{scope:e.__scopeRovingFocusGroup},o.createElement(A.Slot,{scope:e.__scopeRovingFocusGroup},o.createElement(pe,g({},e,{ref:t}))))),pe=o.forwardRef((e,t)=>{const{__scopeRovingFocusGroup:a,orientation:n,loop:r=!1,dir:s,currentTabStopId:c,defaultCurrentTabStopId:b,onCurrentTabStopIdChange:l,onEntryFocus:i,...f}=e,d=o.useRef(null),p=re(t,d),F=V(s),[$=null,T]=G({prop:c,defaultProp:b,onChange:l}),[_,v]=o.useState(!1),m=ce(i),Z=L(a),C=o.useRef(!1),[ee,M]=o.useState(0);return o.useEffect(()=>{const u=d.current;if(u)return u.addEventListener(S,m),()=>u.removeEventListener(S,m)},[m]),o.createElement(ue,{scope:a,orientation:n,dir:F,loop:r,currentTabStopId:$,onItemFocus:o.useCallback(u=>T(u),[T]),onItemShiftTab:o.useCallback(()=>v(!0),[]),onFocusableItemAdd:o.useCallback(()=>M(u=>u+1),[]),onFocusableItemRemove:o.useCallback(()=>M(u=>u-1),[])},o.createElement(E.div,g({tabIndex:_||ee===0?-1:0,"data-orientation":n},f,{ref:p,style:{outline:"none",...e.style},onMouseDown:I(e.onMouseDown,()=>{C.current=!0}),onFocus:I(e.onFocus,u=>{const te=!C.current;if(u.target===u.currentTarget&&te&&!_){const D=new CustomEvent(S,de);if(u.currentTarget.dispatchEvent(D),!D.defaultPrevented){const h=Z().filter(x=>x.focusable),oe=h.find(x=>x.active),ne=h.find(x=>x.id===$),ae=[oe,ne,...h].filter(Boolean).map(x=>x.ref.current);U(ae)}}C.current=!1}),onBlur:I(e.onBlur,()=>v(!1))})))}),ve="RovingFocusGroupItem",me=o.forwardRef((e,t)=>{const{__scopeRovingFocusGroup:a,focusable:n=!0,active:r=!1,tabStopId:s,...c}=e,b=k(),l=s||b,i=le(ve,a),f=i.currentTabStopId===l,d=L(a),{onFocusableItemAdd:p,onFocusableItemRemove:F}=i;return o.useEffect(()=>{if(n)return p(),()=>F()},[n,p,F]),o.createElement(A.ItemSlot,{scope:a,id:l,focusable:n,active:r},o.createElement(E.span,g({tabIndex:f?0:-1,"data-orientation":i.orientation},c,{ref:t,onMouseDown:I(e.onMouseDown,$=>{n?i.onItemFocus(l):$.preventDefault()}),onFocus:I(e.onFocus,()=>i.onItemFocus(l)),onKeyDown:I(e.onKeyDown,$=>{if($.key==="Tab"&&$.shiftKey){i.onItemShiftTab();return}if($.target!==$.currentTarget)return;const T=Te($,i.orientation,i.dir);if(T!==void 0){$.preventDefault();let v=d().filter(m=>m.focusable).map(m=>m.ref.current);if(T==="last")v.reverse();else if(T==="prev"||T==="next"){T==="prev"&&v.reverse();const m=v.indexOf($.currentTarget);v=i.loop?xe(v,m+1):v.slice(m+1)}setTimeout(()=>U(v))}})})))}),ge={ArrowLeft:"prev",ArrowUp:"prev",ArrowRight:"next",ArrowDown:"next",PageUp:"first",Home:"first",PageDown:"last",End:"last"};function Ie(e,t){return t!=="rtl"?e:e==="ArrowLeft"?"ArrowRight":e==="ArrowRight"?"ArrowLeft":e}function Te(e,t,a){const n=Ie(e.key,a);if(!(t==="vertical"&&["ArrowLeft","ArrowRight"].includes(n))&&!(t==="horizontal"&&["ArrowUp","ArrowDown"].includes(n)))return ge[n]}function U(e){const t=document.activeElement;for(const a of e)if(a===t||(a.focus(),document.activeElement!==t))return}function xe(e,t){return e.map((a,n)=>e[(t+n)%e.length])}const Ee=$e,Fe=me,y="horizontal",we=["horizontal","vertical"],j=o.forwardRef((e,t)=>{const{decorative:a,orientation:n=y,...r}=e,s=z(n)?n:y,b=a?{role:"none"}:{"aria-orientation":s==="vertical"?s:void 0,role:"separator"};return o.createElement(E.div,g({"data-orientation":s},b,r,{ref:t}))});j.propTypes={orientation(e,t,a){const n=e[t],r=String(n);return n&&!z(n)?new Error(Re(r,a)):null}};function Re(e,t){return`Invalid prop \`orientation\` of value \`${e}\` supplied to \`${t}\`, expected one of:
  - horizontal
  - vertical

Defaulting to \`${y}\`.`}function z(e){return we.includes(e)}const B=j,_e=o.forwardRef(({className:e,orientation:t="horizontal",decorative:a=!0,...n},r)=>w.jsx(B,{ref:r,decorative:a,orientation:t,className:R("shrink-0 bg-ring/40",t==="horizontal"?"h-[1px] w-full":"h-full w-[1px]",e),...n}));_e.displayName=B.displayName;const Y="Tabs",[Ce,je]=O(Y,[K]),H=K(),[he,P]=Ce(Y),Se=o.forwardRef((e,t)=>{const{__scopeTabs:a,value:n,onValueChange:r,defaultValue:s,orientation:c="horizontal",dir:b,activationMode:l="automatic",...i}=e,f=V(b),[d,p]=G({prop:n,onChange:r,defaultProp:s});return o.createElement(he,{scope:a,baseId:k(),value:d,onValueChange:p,orientation:c,dir:f,activationMode:l},o.createElement(E.div,g({dir:f,"data-orientation":c},i,{ref:t})))}),Ae="TabsList",ye=o.forwardRef((e,t)=>{const{__scopeTabs:a,loop:n=!0,...r}=e,s=P(Ae,a),c=H(a);return o.createElement(Ee,g({asChild:!0},c,{orientation:s.orientation,dir:s.dir,loop:n}),o.createElement(E.div,g({role:"tablist","aria-orientation":s.orientation},r,{ref:t})))}),Ne="TabsTrigger",Pe=o.forwardRef((e,t)=>{const{__scopeTabs:a,value:n,disabled:r=!1,...s}=e,c=P(Ne,a),b=H(a),l=q(c.baseId,n),i=J(c.baseId,n),f=n===c.value;return o.createElement(Fe,g({asChild:!0},b,{focusable:!r,active:f}),o.createElement(E.button,g({type:"button",role:"tab","aria-selected":f,"aria-controls":i,"data-state":f?"active":"inactive","data-disabled":r?"":void 0,disabled:r,id:l},s,{ref:t,onMouseDown:I(e.onMouseDown,d=>{!r&&d.button===0&&d.ctrlKey===!1?c.onValueChange(n):d.preventDefault()}),onKeyDown:I(e.onKeyDown,d=>{[" ","Enter"].includes(d.key)&&c.onValueChange(n)}),onFocus:I(e.onFocus,()=>{const d=c.activationMode!=="manual";!f&&!r&&d&&c.onValueChange(n)})})))}),Me="TabsContent",De=o.forwardRef((e,t)=>{const{__scopeTabs:a,value:n,forceMount:r,children:s,...c}=e,b=P(Me,a),l=q(b.baseId,n),i=J(b.baseId,n),f=n===b.value,d=o.useRef(f);return o.useEffect(()=>{const p=requestAnimationFrame(()=>d.current=!1);return()=>cancelAnimationFrame(p)},[]),o.createElement(se,{present:r||f},({present:p})=>o.createElement(E.div,g({"data-state":f?"active":"inactive","data-orientation":b.orientation,role:"tabpanel","aria-labelledby":l,hidden:!p,id:i,tabIndex:0},c,{ref:t,style:{...e.style,animationDuration:d.current?"0s":void 0}}),p&&s))});function q(e,t){return`${e}-trigger-${t}`}function J(e,t){return`${e}-content-${t}`}const Oe=Se,Q=ye,W=Pe,X=De,ze=Oe,Ge=o.forwardRef(({className:e,...t},a)=>w.jsx(Q,{ref:a,className:R("inline-flex h-10 items-center justify-center rounded-md p-1 text-muted-foreground",e),...t}));Ge.displayName=Q.displayName;const ke=o.forwardRef(({className:e,...t},a)=>w.jsx(W,{ref:a,className:R("inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:border data-[state=inactive]:border data-[state=inactive]:border-muted data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm data-[state=inactive]:hover:bg-secondary/80",e),...t}));ke.displayName=W.displayName;const Ve=o.forwardRef(({className:e,...t},a)=>w.jsx(X,{ref:a,className:R("mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",e),...t}));Ve.displayName=X.displayName;export{K as $,_e as S,ze as T,Ge as a,ke as b,Ve as c,Ee as d,Fe as e};
