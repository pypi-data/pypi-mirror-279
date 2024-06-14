import{r as It}from"./recharts-C4M6_t20.js";import{r as u,e as be,a as O}from"./react-D_Tw0keN.js";function kt(e){var t=Object.create(null);return function(r){return t[r]===void 0&&(t[r]=e(r)),t[r]}}function At(e){if(e.sheet)return e.sheet;for(var t=0;t<document.styleSheets.length;t++)if(document.styleSheets[t].ownerNode===e)return document.styleSheets[t]}function Ot(e){var t=document.createElement("style");return t.setAttribute("data-emotion",e.key),e.nonce!==void 0&&t.setAttribute("nonce",e.nonce),t.appendChild(document.createTextNode("")),t.setAttribute("data-s",""),t}var Rt=function(){function e(r){var n=this;this._insertTag=function(a){var s;n.tags.length===0?n.insertionPoint?s=n.insertionPoint.nextSibling:n.prepend?s=n.container.firstChild:s=n.before:s=n.tags[n.tags.length-1].nextSibling,n.container.insertBefore(a,s),n.tags.push(a)},this.isSpeedy=r.speedy===void 0?!0:r.speedy,this.tags=[],this.ctr=0,this.nonce=r.nonce,this.key=r.key,this.container=r.container,this.prepend=r.prepend,this.insertionPoint=r.insertionPoint,this.before=null}var t=e.prototype;return t.hydrate=function(n){n.forEach(this._insertTag)},t.insert=function(n){this.ctr%(this.isSpeedy?65e3:1)===0&&this._insertTag(Ot(this));var a=this.tags[this.tags.length-1];if(this.isSpeedy){var s=At(a);try{s.insertRule(n,s.cssRules.length)}catch{}}else a.appendChild(document.createTextNode(n));this.ctr++},t.flush=function(){this.tags.forEach(function(n){return n.parentNode&&n.parentNode.removeChild(n)}),this.tags=[],this.ctr=0},e}(),I="-ms-",ge="-moz-",x="-webkit-",et="comm",Ie="rule",ke="decl",Nt="@import",tt="@keyframes",Ft="@layer",Mt=Math.abs,ve=String.fromCharCode,Dt=Object.assign;function Lt(e,t){return $(e,0)^45?(((t<<2^$(e,0))<<2^$(e,1))<<2^$(e,2))<<2^$(e,3):0}function rt(e){return e.trim()}function jt(e,t){return(e=t.exec(e))?e[0]:e}function w(e,t,r){return e.replace(t,r)}function Te(e,t){return e.indexOf(t)}function $(e,t){return e.charCodeAt(t)|0}function ne(e,t,r){return e.slice(t,r)}function j(e){return e.length}function Ae(e){return e.length}function le(e,t){return t.push(e),e}function _t(e,t){return e.map(t).join("")}var ye=1,Q=1,nt=0,N=0,T=0,ee="";function xe(e,t,r,n,a,s,i){return{value:e,root:t,parent:r,type:n,props:a,children:s,line:ye,column:Q,length:i,return:""}}function te(e,t){return Dt(xe("",null,null,"",null,null,0),e,{length:-e.length},t)}function Ut(){return T}function Wt(){return T=N>0?$(ee,--N):0,Q--,T===10&&(Q=1,ye--),T}function F(){return T=N<nt?$(ee,N++):0,Q++,T===10&&(Q=1,ye++),T}function U(){return $(ee,N)}function de(){return N}function ue(e,t){return ne(ee,e,t)}function ae(e){switch(e){case 0:case 9:case 10:case 13:case 32:return 5;case 33:case 43:case 44:case 47:case 62:case 64:case 126:case 59:case 123:case 125:return 4;case 58:return 3;case 34:case 39:case 40:case 91:return 2;case 41:case 93:return 1}return 0}function at(e){return ye=Q=1,nt=j(ee=e),N=0,[]}function st(e){return ee="",e}function pe(e){return rt(ue(N-1,Ce(e===91?e+2:e===40?e+1:e)))}function Ht(e){for(;(T=U())&&T<33;)F();return ae(e)>2||ae(T)>3?"":" "}function Bt(e,t){for(;--t&&F()&&!(T<48||T>102||T>57&&T<65||T>70&&T<97););return ue(e,de()+(t<6&&U()==32&&F()==32))}function Ce(e){for(;F();)switch(T){case e:return N;case 34:case 39:e!==34&&e!==39&&Ce(T);break;case 40:e===41&&Ce(e);break;case 92:F();break}return N}function Gt(e,t){for(;F()&&e+T!==57;)if(e+T===84&&U()===47)break;return"/*"+ue(t,N-1)+"*"+ve(e===47?e:F())}function Kt(e){for(;!ae(U());)F();return ue(e,N)}function qt(e){return st(he("",null,null,null,[""],e=at(e),0,[0],e))}function he(e,t,r,n,a,s,i,o,c){for(var d=0,l=0,p=i,f=0,g=0,v=0,m=1,y=1,b=1,h=0,P="",M=a,A=s,R=n,E=P;y;)switch(v=h,h=F()){case 40:if(v!=108&&$(E,p-1)==58){Te(E+=w(pe(h),"&","&\f"),"&\f")!=-1&&(b=-1);break}case 34:case 39:case 91:E+=pe(h);break;case 9:case 10:case 13:case 32:E+=Ht(v);break;case 92:E+=Bt(de()-1,7);continue;case 47:switch(U()){case 42:case 47:le(zt(Gt(F(),de()),t,r),c);break;default:E+="/"}break;case 123*m:o[d++]=j(E)*b;case 125*m:case 59:case 0:switch(h){case 0:case 125:y=0;case 59+l:b==-1&&(E=w(E,/\f/g,"")),g>0&&j(E)-p&&le(g>32?Be(E+";",n,r,p-1):Be(w(E," ","")+";",n,r,p-2),c);break;case 59:E+=";";default:if(le(R=He(E,t,r,d,l,a,o,P,M=[],A=[],p),s),h===123)if(l===0)he(E,t,R,R,M,s,p,o,A);else switch(f===99&&$(E,3)===110?100:f){case 100:case 108:case 109:case 115:he(e,R,R,n&&le(He(e,R,R,0,0,a,o,P,a,M=[],p),A),a,A,p,o,n?M:A);break;default:he(E,R,R,R,[""],A,0,o,A)}}d=l=g=0,m=b=1,P=E="",p=i;break;case 58:p=1+j(E),g=v;default:if(m<1){if(h==123)--m;else if(h==125&&m++==0&&Wt()==125)continue}switch(E+=ve(h),h*m){case 38:b=l>0?1:(E+="\f",-1);break;case 44:o[d++]=(j(E)-1)*b,b=1;break;case 64:U()===45&&(E+=pe(F())),f=U(),l=p=j(P=E+=Kt(de())),h++;break;case 45:v===45&&j(E)==2&&(m=0)}}return s}function He(e,t,r,n,a,s,i,o,c,d,l){for(var p=a-1,f=a===0?s:[""],g=Ae(f),v=0,m=0,y=0;v<n;++v)for(var b=0,h=ne(e,p+1,p=Mt(m=i[v])),P=e;b<g;++b)(P=rt(m>0?f[b]+" "+h:w(h,/&\f/g,f[b])))&&(c[y++]=P);return xe(e,t,r,a===0?Ie:o,c,d,l)}function zt(e,t,r){return xe(e,t,r,et,ve(Ut()),ne(e,2,-2),0)}function Be(e,t,r,n){return xe(e,t,r,ke,ne(e,0,n),ne(e,n+1,-1),n)}function Z(e,t){for(var r="",n=Ae(e),a=0;a<n;a++)r+=t(e[a],a,e,t)||"";return r}function Vt(e,t,r,n){switch(e.type){case Ft:if(e.children.length)break;case Nt:case ke:return e.return=e.return||e.value;case et:return"";case tt:return e.return=e.value+"{"+Z(e.children,n)+"}";case Ie:e.value=e.props.join(",")}return j(r=Z(e.children,n))?e.return=e.value+"{"+r+"}":""}function Yt(e){var t=Ae(e);return function(r,n,a,s){for(var i="",o=0;o<t;o++)i+=e[o](r,n,a,s)||"";return i}}function Xt(e){return function(t){t.root||(t=t.return)&&e(t)}}var Zt=function(t,r,n){for(var a=0,s=0;a=s,s=U(),a===38&&s===12&&(r[n]=1),!ae(s);)F();return ue(t,N)},Qt=function(t,r){var n=-1,a=44;do switch(ae(a)){case 0:a===38&&U()===12&&(r[n]=1),t[n]+=Zt(N-1,r,n);break;case 2:t[n]+=pe(a);break;case 4:if(a===44){t[++n]=U()===58?"&\f":"",r[n]=t[n].length;break}default:t[n]+=ve(a)}while(a=F());return t},Jt=function(t,r){return st(Qt(at(t),r))},Ge=new WeakMap,er=function(t){if(!(t.type!=="rule"||!t.parent||t.length<1)){for(var r=t.value,n=t.parent,a=t.column===n.column&&t.line===n.line;n.type!=="rule";)if(n=n.parent,!n)return;if(!(t.props.length===1&&r.charCodeAt(0)!==58&&!Ge.get(n))&&!a){Ge.set(t,!0);for(var s=[],i=Jt(r,s),o=n.props,c=0,d=0;c<i.length;c++)for(var l=0;l<o.length;l++,d++)t.props[d]=s[c]?i[c].replace(/&\f/g,o[l]):o[l]+" "+i[c]}}},tr=function(t){if(t.type==="decl"){var r=t.value;r.charCodeAt(0)===108&&r.charCodeAt(2)===98&&(t.return="",t.value="")}};function it(e,t){switch(Lt(e,t)){case 5103:return x+"print-"+e+e;case 5737:case 4201:case 3177:case 3433:case 1641:case 4457:case 2921:case 5572:case 6356:case 5844:case 3191:case 6645:case 3005:case 6391:case 5879:case 5623:case 6135:case 4599:case 4855:case 4215:case 6389:case 5109:case 5365:case 5621:case 3829:return x+e+e;case 5349:case 4246:case 4810:case 6968:case 2756:return x+e+ge+e+I+e+e;case 6828:case 4268:return x+e+I+e+e;case 6165:return x+e+I+"flex-"+e+e;case 5187:return x+e+w(e,/(\w+).+(:[^]+)/,x+"box-$1$2"+I+"flex-$1$2")+e;case 5443:return x+e+I+"flex-item-"+w(e,/flex-|-self/,"")+e;case 4675:return x+e+I+"flex-line-pack"+w(e,/align-content|flex-|-self/,"")+e;case 5548:return x+e+I+w(e,"shrink","negative")+e;case 5292:return x+e+I+w(e,"basis","preferred-size")+e;case 6060:return x+"box-"+w(e,"-grow","")+x+e+I+w(e,"grow","positive")+e;case 4554:return x+w(e,/([^-])(transform)/g,"$1"+x+"$2")+e;case 6187:return w(w(w(e,/(zoom-|grab)/,x+"$1"),/(image-set)/,x+"$1"),e,"")+e;case 5495:case 3959:return w(e,/(image-set\([^]*)/,x+"$1$`$1");case 4968:return w(w(e,/(.+:)(flex-)?(.*)/,x+"box-pack:$3"+I+"flex-pack:$3"),/s.+-b[^;]+/,"justify")+x+e+e;case 4095:case 3583:case 4068:case 2532:return w(e,/(.+)-inline(.+)/,x+"$1$2")+e;case 8116:case 7059:case 5753:case 5535:case 5445:case 5701:case 4933:case 4677:case 5533:case 5789:case 5021:case 4765:if(j(e)-1-t>6)switch($(e,t+1)){case 109:if($(e,t+4)!==45)break;case 102:return w(e,/(.+:)(.+)-([^]+)/,"$1"+x+"$2-$3$1"+ge+($(e,t+3)==108?"$3":"$2-$3"))+e;case 115:return~Te(e,"stretch")?it(w(e,"stretch","fill-available"),t)+e:e}break;case 4949:if($(e,t+1)!==115)break;case 6444:switch($(e,j(e)-3-(~Te(e,"!important")&&10))){case 107:return w(e,":",":"+x)+e;case 101:return w(e,/(.+:)([^;!]+)(;|!.+)?/,"$1"+x+($(e,14)===45?"inline-":"")+"box$3$1"+x+"$2$3$1"+I+"$2box$3")+e}break;case 5936:switch($(e,t+11)){case 114:return x+e+I+w(e,/[svh]\w+-[tblr]{2}/,"tb")+e;case 108:return x+e+I+w(e,/[svh]\w+-[tblr]{2}/,"tb-rl")+e;case 45:return x+e+I+w(e,/[svh]\w+-[tblr]{2}/,"lr")+e}return x+e+I+e+e}return e}var rr=function(t,r,n,a){if(t.length>-1&&!t.return)switch(t.type){case ke:t.return=it(t.value,t.length);break;case tt:return Z([te(t,{value:w(t.value,"@","@"+x)})],a);case Ie:if(t.length)return _t(t.props,function(s){switch(jt(s,/(::plac\w+|:read-\w+)/)){case":read-only":case":read-write":return Z([te(t,{props:[w(s,/:(read-\w+)/,":"+ge+"$1")]})],a);case"::placeholder":return Z([te(t,{props:[w(s,/:(plac\w+)/,":"+x+"input-$1")]}),te(t,{props:[w(s,/:(plac\w+)/,":"+ge+"$1")]}),te(t,{props:[w(s,/:(plac\w+)/,I+"input-$1")]})],a)}return""})}},nr=[rr],ar=function(t){var r=t.key;if(r==="css"){var n=document.querySelectorAll("style[data-emotion]:not([data-s])");Array.prototype.forEach.call(n,function(m){var y=m.getAttribute("data-emotion");y.indexOf(" ")!==-1&&(document.head.appendChild(m),m.setAttribute("data-s",""))})}var a=t.stylisPlugins||nr,s={},i,o=[];i=t.container||document.head,Array.prototype.forEach.call(document.querySelectorAll('style[data-emotion^="'+r+' "]'),function(m){for(var y=m.getAttribute("data-emotion").split(" "),b=1;b<y.length;b++)s[y[b]]=!0;o.push(m)});var c,d=[er,tr];{var l,p=[Vt,Xt(function(m){l.insert(m)})],f=Yt(d.concat(a,p)),g=function(y){return Z(qt(y),f)};c=function(y,b,h,P){l=h,g(y?y+"{"+b.styles+"}":b.styles),P&&(v.inserted[b.name]=!0)}}var v={key:r,sheet:new Rt({key:r,container:i,nonce:t.nonce,speedy:t.speedy,prepend:t.prepend,insertionPoint:t.insertionPoint}),nonce:t.nonce,inserted:s,registered:{},insert:c};return v.sheet.hydrate(o),v},ot=It,sr={$$typeof:!0,render:!0,defaultProps:!0,displayName:!0,propTypes:!0},ir={$$typeof:!0,compare:!0,defaultProps:!0,displayName:!0,propTypes:!0,type:!0},ut={};ut[ot.ForwardRef]=sr;ut[ot.Memo]=ir;var or=!0;function ur(e,t,r){var n="";return r.split(" ").forEach(function(a){e[a]!==void 0?t.push(e[a]+";"):n+=a+" "}),n}var ct=function(t,r,n){var a=t.key+"-"+r.name;(n===!1||or===!1)&&t.registered[a]===void 0&&(t.registered[a]=r.styles)},lt=function(t,r,n){ct(t,r,n);var a=t.key+"-"+r.name;if(t.inserted[r.name]===void 0){var s=r;do t.insert(r===s?"."+a:"",s,t.sheet,!0),s=s.next;while(s!==void 0)}};function cr(e){for(var t=0,r,n=0,a=e.length;a>=4;++n,a-=4)r=e.charCodeAt(n)&255|(e.charCodeAt(++n)&255)<<8|(e.charCodeAt(++n)&255)<<16|(e.charCodeAt(++n)&255)<<24,r=(r&65535)*1540483477+((r>>>16)*59797<<16),r^=r>>>24,t=(r&65535)*1540483477+((r>>>16)*59797<<16)^(t&65535)*1540483477+((t>>>16)*59797<<16);switch(a){case 3:t^=(e.charCodeAt(n+2)&255)<<16;case 2:t^=(e.charCodeAt(n+1)&255)<<8;case 1:t^=e.charCodeAt(n)&255,t=(t&65535)*1540483477+((t>>>16)*59797<<16)}return t^=t>>>13,t=(t&65535)*1540483477+((t>>>16)*59797<<16),((t^t>>>15)>>>0).toString(36)}var lr={animationIterationCount:1,aspectRatio:1,borderImageOutset:1,borderImageSlice:1,borderImageWidth:1,boxFlex:1,boxFlexGroup:1,boxOrdinalGroup:1,columnCount:1,columns:1,flex:1,flexGrow:1,flexPositive:1,flexShrink:1,flexNegative:1,flexOrder:1,gridRow:1,gridRowEnd:1,gridRowSpan:1,gridRowStart:1,gridColumn:1,gridColumnEnd:1,gridColumnSpan:1,gridColumnStart:1,msGridRow:1,msGridRowSpan:1,msGridColumn:1,msGridColumnSpan:1,fontWeight:1,lineHeight:1,opacity:1,order:1,orphans:1,tabSize:1,widows:1,zIndex:1,zoom:1,WebkitLineClamp:1,fillOpacity:1,floodOpacity:1,stopOpacity:1,strokeDasharray:1,strokeDashoffset:1,strokeMiterlimit:1,strokeOpacity:1,strokeWidth:1},fr=/[A-Z]|^ms/g,dr=/_EMO_([^_]+?)_([^]*?)_EMO_/g,ft=function(t){return t.charCodeAt(1)===45},Ke=function(t){return t!=null&&typeof t!="boolean"},Ee=kt(function(e){return ft(e)?e:e.replace(fr,"-$&").toLowerCase()}),qe=function(t,r){switch(t){case"animation":case"animationName":if(typeof r=="string")return r.replace(dr,function(n,a,s){return _={name:a,styles:s,next:_},a})}return lr[t]!==1&&!ft(t)&&typeof r=="number"&&r!==0?r+"px":r};function se(e,t,r){if(r==null)return"";if(r.__emotion_styles!==void 0)return r;switch(typeof r){case"boolean":return"";case"object":{if(r.anim===1)return _={name:r.name,styles:r.styles,next:_},r.name;if(r.styles!==void 0){var n=r.next;if(n!==void 0)for(;n!==void 0;)_={name:n.name,styles:n.styles,next:_},n=n.next;var a=r.styles+";";return a}return pr(e,t,r)}case"function":{if(e!==void 0){var s=_,i=r(e);return _=s,se(e,t,i)}break}}if(t==null)return r;var o=t[r];return o!==void 0?o:r}function pr(e,t,r){var n="";if(Array.isArray(r))for(var a=0;a<r.length;a++)n+=se(e,t,r[a])+";";else for(var s in r){var i=r[s];if(typeof i!="object")t!=null&&t[i]!==void 0?n+=s+"{"+t[i]+"}":Ke(i)&&(n+=Ee(s)+":"+qe(s,i)+";");else if(Array.isArray(i)&&typeof i[0]=="string"&&(t==null||t[i[0]]===void 0))for(var o=0;o<i.length;o++)Ke(i[o])&&(n+=Ee(s)+":"+qe(s,i[o])+";");else{var c=se(e,t,i);switch(s){case"animation":case"animationName":{n+=Ee(s)+":"+c+";";break}default:n+=s+"{"+c+"}"}}}return n}var ze=/label:\s*([^\s;\n{]+)\s*(;|$)/g,_,Oe=function(t,r,n){if(t.length===1&&typeof t[0]=="object"&&t[0]!==null&&t[0].styles!==void 0)return t[0];var a=!0,s="";_=void 0;var i=t[0];i==null||i.raw===void 0?(a=!1,s+=se(n,r,i)):s+=i[0];for(var o=1;o<t.length;o++)s+=se(n,r,t[o]),a&&(s+=i[o]);ze.lastIndex=0;for(var c="",d;(d=ze.exec(s))!==null;)c+="-"+d[1];var l=cr(s)+c;return{name:l,styles:s,next:_}},hr=function(t){return t()},dt=be.useInsertionEffect?be.useInsertionEffect:!1,mr=dt||hr,Ve=dt||u.useLayoutEffect,Re={}.hasOwnProperty,pt=u.createContext(typeof HTMLElement<"u"?ar({key:"css"}):null);pt.Provider;var ht=function(t){return u.forwardRef(function(r,n){var a=u.useContext(pt);return t(r,a,n)})},mt=u.createContext({}),$e="__EMOTION_TYPE_PLEASE_DO_NOT_USE__",br=function(t,r){var n={};for(var a in r)Re.call(r,a)&&(n[a]=r[a]);return n[$e]=t,n},gr=function(t){var r=t.cache,n=t.serialized,a=t.isStringTag;return ct(r,n,a),mr(function(){return lt(r,n,a)}),null},vr=ht(function(e,t,r){var n=e.css;typeof n=="string"&&t.registered[n]!==void 0&&(n=t.registered[n]);var a=e[$e],s=[n],i="";typeof e.className=="string"?i=ur(t.registered,s,e.className):e.className!=null&&(i=e.className+" ");var o=Oe(s,void 0,u.useContext(mt));i+=t.key+"-"+o.name;var c={};for(var d in e)Re.call(e,d)&&d!=="css"&&d!==$e&&(c[d]=e[d]);return c.ref=r,c.className=i,u.createElement(u.Fragment,null,u.createElement(gr,{cache:t,serialized:o,isStringTag:typeof a=="string"}),u.createElement(a,c))}),yr=vr,Nn=function(t,r){var n=arguments;if(r==null||!Re.call(r,"css"))return u.createElement.apply(void 0,n);var a=n.length,s=new Array(a);s[0]=yr,s[1]=br(t,r);for(var i=2;i<a;i++)s[i]=n[i];return u.createElement.apply(null,s)},Fn=ht(function(e,t){var r=e.styles,n=Oe([r],void 0,u.useContext(mt)),a=u.useRef();return Ve(function(){var s=t.key+"-global",i=new t.sheet.constructor({key:s,nonce:t.sheet.nonce,container:t.sheet.container,speedy:t.sheet.isSpeedy}),o=!1,c=document.querySelector('style[data-emotion="'+s+" "+n.name+'"]');return t.sheet.tags.length&&(i.before=t.sheet.tags[0]),c!==null&&(o=!0,c.setAttribute("data-emotion",s),i.hydrate([c])),a.current=[i,o],function(){i.flush()}},[t]),Ve(function(){var s=a.current,i=s[0],o=s[1];if(o){s[1]=!1;return}if(n.next!==void 0&&lt(t,n.next,!0),i.tags.length){var c=i.tags[i.tags.length-1].nextElementSibling;i.before=c,i.flush()}t.insert("",n,i,!1)},[t,n.name]),null});function Mn(){for(var e=arguments.length,t=new Array(e),r=0;r<e;r++)t[r]=arguments[r];return Oe(t)}var xr=Object.defineProperty,wr=(e,t,r)=>t in e?xr(e,t,{enumerable:!0,configurable:!0,writable:!0,value:r}):e[t]=r,Se=(e,t,r)=>(wr(e,typeof t!="symbol"?t+"":t,r),r);let Er=class{constructor(){Se(this,"current",this.detect()),Se(this,"handoffState","pending"),Se(this,"currentId",0)}set(t){this.current!==t&&(this.handoffState="pending",this.currentId=0,this.current=t)}reset(){this.set(this.detect())}nextId(){return++this.currentId}get isServer(){return this.current==="server"}get isClient(){return this.current==="client"}detect(){return typeof window>"u"||typeof document>"u"?"server":"client"}handoff(){this.handoffState==="pending"&&(this.handoffState="complete")}get isHandoffComplete(){return this.handoffState==="complete"}},V=new Er,B=(e,t)=>{V.isServer?u.useEffect(e,t):u.useLayoutEffect(e,t)};function me(e){let t=u.useRef(e);return B(()=>{t.current=e},[e]),t}let D=function(e){let t=me(e);return O.useCallback((...r)=>t.current(...r),[t])};function Sr(e){typeof queueMicrotask=="function"?queueMicrotask(e):Promise.resolve().then(e).catch(t=>setTimeout(()=>{throw t}))}function Pr(){let e=typeof document>"u";return"useSyncExternalStore"in be?(t=>t.useSyncExternalStore)(be)(()=>()=>{},()=>!1,()=>!e):!1}function Tr(){let e=Pr(),[t,r]=u.useState(V.isHandoffComplete);return t&&V.isHandoffComplete===!1&&r(!1),u.useEffect(()=>{t!==!0&&r(!0)},[t]),u.useEffect(()=>V.handoff(),[]),e?!1:t}var Ye;let we=(Ye=O.useId)!=null?Ye:function(){let e=Tr(),[t,r]=O.useState(e?()=>V.nextId():null);return B(()=>{t===null&&r(V.nextId())},[t]),t!=null?""+t:void 0};function W(e,t,...r){if(e in t){let a=t[e];return typeof a=="function"?a(...r):a}let n=new Error(`Tried to handle "${e}" but there is no handler defined. Only defined handlers are: ${Object.keys(t).map(a=>`"${a}"`).join(", ")}.`);throw Error.captureStackTrace&&Error.captureStackTrace(n,W),n}function bt(e){return V.isServer?null:e instanceof Node?e.ownerDocument:e!=null&&e.hasOwnProperty("current")&&e.current instanceof Node?e.current.ownerDocument:document}let Cr=["[contentEditable=true]","[tabindex]","a[href]","area[href]","button:not([disabled])","iframe","input:not([disabled])","select:not([disabled])","textarea:not([disabled])"].map(e=>`${e}:not([tabindex='-1'])`).join(",");var L=(e=>(e[e.First=1]="First",e[e.Previous=2]="Previous",e[e.Next=4]="Next",e[e.Last=8]="Last",e[e.WrapAround=16]="WrapAround",e[e.NoScroll=32]="NoScroll",e))(L||{}),re=(e=>(e[e.Error=0]="Error",e[e.Overflow=1]="Overflow",e[e.Success=2]="Success",e[e.Underflow=3]="Underflow",e))(re||{}),$r=(e=>(e[e.Previous=-1]="Previous",e[e.Next=1]="Next",e))($r||{});function Ir(e=document.body){return e==null?[]:Array.from(e.querySelectorAll(Cr)).sort((t,r)=>Math.sign((t.tabIndex||Number.MAX_SAFE_INTEGER)-(r.tabIndex||Number.MAX_SAFE_INTEGER)))}var kr=(e=>(e[e.Strict=0]="Strict",e[e.Loose=1]="Loose",e))(kr||{}),Ar=(e=>(e[e.Keyboard=0]="Keyboard",e[e.Mouse=1]="Mouse",e))(Ar||{});typeof window<"u"&&typeof document<"u"&&(document.addEventListener("keydown",e=>{e.metaKey||e.altKey||e.ctrlKey||(document.documentElement.dataset.headlessuiFocusVisible="")},!0),document.addEventListener("click",e=>{e.detail===1?delete document.documentElement.dataset.headlessuiFocusVisible:e.detail===0&&(document.documentElement.dataset.headlessuiFocusVisible="")},!0));let Or=["textarea","input"].join(",");function Rr(e){var t,r;return(r=(t=e==null?void 0:e.matches)==null?void 0:t.call(e,Or))!=null?r:!1}function X(e,t=r=>r){return e.slice().sort((r,n)=>{let a=t(r),s=t(n);if(a===null||s===null)return 0;let i=a.compareDocumentPosition(s);return i&Node.DOCUMENT_POSITION_FOLLOWING?-1:i&Node.DOCUMENT_POSITION_PRECEDING?1:0})}function Y(e,t,{sorted:r=!0,relativeTo:n=null,skipElements:a=[]}={}){let s=Array.isArray(e)?e.length>0?e[0].ownerDocument:document:e.ownerDocument,i=Array.isArray(e)?r?X(e):e:Ir(e);a.length>0&&i.length>1&&(i=i.filter(g=>!a.includes(g))),n=n??s.activeElement;let o=(()=>{if(t&5)return 1;if(t&10)return-1;throw new Error("Missing Focus.First, Focus.Previous, Focus.Next or Focus.Last")})(),c=(()=>{if(t&1)return 0;if(t&2)return Math.max(0,i.indexOf(n))-1;if(t&4)return Math.max(0,i.indexOf(n))+1;if(t&8)return i.length-1;throw new Error("Missing Focus.First, Focus.Previous, Focus.Next or Focus.Last")})(),d=t&32?{preventScroll:!0}:{},l=0,p=i.length,f;do{if(l>=p||l+p<=0)return 0;let g=c+l;if(t&16)g=(g+p)%p;else{if(g<0)return 3;if(g>=p)return 1}f=i[g],f==null||f.focus(d),l+=o}while(f!==s.activeElement);return t&6&&Rr(f)&&f.select(),2}function Xe(e){var t;if(e.type)return e.type;let r=(t=e.as)!=null?t:"button";if(typeof r=="string"&&r.toLowerCase()==="button")return"button"}function gt(e,t){let[r,n]=u.useState(()=>Xe(e));return B(()=>{n(Xe(e))},[e.type,e.as]),B(()=>{r||t.current&&t.current instanceof HTMLButtonElement&&!t.current.hasAttribute("type")&&n("button")},[r,t]),r}let vt=Symbol();function Nr(e,t=!0){return Object.assign(e,{[vt]:t})}function z(...e){let t=u.useRef(e);u.useEffect(()=>{t.current=e},[e]);let r=D(n=>{for(let a of t.current)a!=null&&(typeof a=="function"?a(n):a.current=n)});return e.every(n=>n==null||(n==null?void 0:n[vt]))?void 0:r}function Ze(...e){return Array.from(new Set(e.flatMap(t=>typeof t=="string"?t.split(" "):[]))).filter(Boolean).join(" ")}var ie=(e=>(e[e.None=0]="None",e[e.RenderStrategy=1]="RenderStrategy",e[e.Static=2]="Static",e))(ie||{}),Fr=(e=>(e[e.Unmount=0]="Unmount",e[e.Hidden=1]="Hidden",e))(Fr||{});function G({ourProps:e,theirProps:t,slot:r,defaultTag:n,features:a,visible:s=!0,name:i,mergeRefs:o}){o=o??Mr;let c=xt(t,e);if(s)return fe(c,r,n,i,o);let d=a??0;if(d&2){let{static:l=!1,...p}=c;if(l)return fe(p,r,n,i,o)}if(d&1){let{unmount:l=!0,...p}=c;return W(l?0:1,{0(){return null},1(){return fe({...p,hidden:!0,style:{display:"none"}},r,n,i,o)}})}return fe(c,r,n,i,o)}function fe(e,t={},r,n,a){let{as:s=r,children:i,refName:o="ref",...c}=Pe(e,["unmount","static"]),d=e.ref!==void 0?{[o]:e.ref}:{},l=typeof i=="function"?i(t):i;"className"in c&&c.className&&typeof c.className=="function"&&(c.className=c.className(t));let p={};if(t){let f=!1,g=[];for(let[v,m]of Object.entries(t))typeof m=="boolean"&&(f=!0),m===!0&&g.push(v);f&&(p["data-headlessui-state"]=g.join(" "))}if(s===u.Fragment&&Object.keys(Qe(c)).length>0){if(!u.isValidElement(l)||Array.isArray(l)&&l.length>1)throw new Error(['Passing props on "Fragment"!',"",`The current component <${n} /> is rendering a "Fragment".`,"However we need to passthrough the following props:",Object.keys(c).map(m=>`  - ${m}`).join(`
`),"","You can apply a few solutions:",['Add an `as="..."` prop, to ensure that we render an actual element instead of a "Fragment".',"Render a single element as the child so that we can forward the props onto that element."].map(m=>`  - ${m}`).join(`
`)].join(`
`));let f=l.props,g=typeof(f==null?void 0:f.className)=="function"?(...m)=>Ze(f==null?void 0:f.className(...m),c.className):Ze(f==null?void 0:f.className,c.className),v=g?{className:g}:{};return u.cloneElement(l,Object.assign({},xt(l.props,Qe(Pe(c,["ref"]))),p,d,{ref:a(l.ref,d.ref)},v))}return u.createElement(s,Object.assign({},Pe(c,["ref"]),s!==u.Fragment&&d,s!==u.Fragment&&p),l)}function yt(){let e=u.useRef([]),t=u.useCallback(r=>{for(let n of e.current)n!=null&&(typeof n=="function"?n(r):n.current=r)},[]);return(...r)=>{if(!r.every(n=>n==null))return e.current=r,t}}function Mr(...e){return e.every(t=>t==null)?void 0:t=>{for(let r of e)r!=null&&(typeof r=="function"?r(t):r.current=t)}}function xt(...e){if(e.length===0)return{};if(e.length===1)return e[0];let t={},r={};for(let n of e)for(let a in n)a.startsWith("on")&&typeof n[a]=="function"?(r[a]!=null||(r[a]=[]),r[a].push(n[a])):t[a]=n[a];if(t.disabled||t["aria-disabled"])return Object.assign(t,Object.fromEntries(Object.keys(r).map(n=>[n,void 0])));for(let n in r)Object.assign(t,{[n](a,...s){let i=r[n];for(let o of i){if((a instanceof Event||(a==null?void 0:a.nativeEvent)instanceof Event)&&a.defaultPrevented)return;o(a,...s)}}});return t}function K(e){var t;return Object.assign(u.forwardRef(e),{displayName:(t=e.displayName)!=null?t:e.name})}function Qe(e){let t=Object.assign({},e);for(let r in t)t[r]===void 0&&delete t[r];return t}function Pe(e,t=[]){let r=Object.assign({},e);for(let n of t)n in r&&delete r[n];return r}let Dr="div";var wt=(e=>(e[e.None=1]="None",e[e.Focusable=2]="Focusable",e[e.Hidden=4]="Hidden",e))(wt||{});function Lr(e,t){var r;let{features:n=1,...a}=e,s={ref:t,"aria-hidden":(n&2)===2?!0:(r=a["aria-hidden"])!=null?r:void 0,style:{position:"fixed",top:1,left:1,width:1,height:0,padding:0,margin:-1,overflow:"hidden",clip:"rect(0, 0, 0, 0)",whiteSpace:"nowrap",borderWidth:"0",...(n&4)===4&&(n&2)!==2&&{display:"none"}}};return G({ourProps:s,theirProps:a,slot:{},defaultTag:Dr,name:"Hidden"})}let Et=K(Lr),Ne=u.createContext(null);Ne.displayName="OpenClosedContext";var oe=(e=>(e[e.Open=1]="Open",e[e.Closed=2]="Closed",e[e.Closing=4]="Closing",e[e.Opening=8]="Opening",e))(oe||{});function jr(){return u.useContext(Ne)}function _r({value:e,children:t}){return O.createElement(Ne.Provider,{value:e},t)}function Ur(e){let t=e.parentElement,r=null;for(;t&&!(t instanceof HTMLFieldSetElement);)t instanceof HTMLLegendElement&&(r=t),t=t.parentElement;let n=(t==null?void 0:t.getAttribute("disabled"))==="";return n&&Wr(r)?!1:n}function Wr(e){if(!e)return!1;let t=e.previousElementSibling;for(;t!==null;){if(t instanceof HTMLLegendElement)return!1;t=t.previousElementSibling}return!0}var k=(e=>(e.Space=" ",e.Enter="Enter",e.Escape="Escape",e.Backspace="Backspace",e.Delete="Delete",e.ArrowLeft="ArrowLeft",e.ArrowUp="ArrowUp",e.ArrowRight="ArrowRight",e.ArrowDown="ArrowDown",e.Home="Home",e.End="End",e.PageUp="PageUp",e.PageDown="PageDown",e.Tab="Tab",e))(k||{});function Hr(){let e=u.useRef(!1);return B(()=>(e.current=!0,()=>{e.current=!1}),[]),e}var Je;let Br=(Je=O.startTransition)!=null?Je:function(e){e()};var Gr=(e=>(e[e.Open=0]="Open",e[e.Closed=1]="Closed",e))(Gr||{}),Kr=(e=>(e[e.ToggleDisclosure=0]="ToggleDisclosure",e[e.CloseDisclosure=1]="CloseDisclosure",e[e.SetButtonId=2]="SetButtonId",e[e.SetPanelId=3]="SetPanelId",e[e.LinkPanel=4]="LinkPanel",e[e.UnlinkPanel=5]="UnlinkPanel",e))(Kr||{});let qr={0:e=>({...e,disclosureState:W(e.disclosureState,{0:1,1:0})}),1:e=>e.disclosureState===1?e:{...e,disclosureState:1},4(e){return e.linkedPanel===!0?e:{...e,linkedPanel:!0}},5(e){return e.linkedPanel===!1?e:{...e,linkedPanel:!1}},2(e,t){return e.buttonId===t.buttonId?e:{...e,buttonId:t.buttonId}},3(e,t){return e.panelId===t.panelId?e:{...e,panelId:t.panelId}}},Fe=u.createContext(null);Fe.displayName="DisclosureContext";function Me(e){let t=u.useContext(Fe);if(t===null){let r=new Error(`<${e} /> is missing a parent <Disclosure /> component.`);throw Error.captureStackTrace&&Error.captureStackTrace(r,Me),r}return t}let De=u.createContext(null);De.displayName="DisclosureAPIContext";function St(e){let t=u.useContext(De);if(t===null){let r=new Error(`<${e} /> is missing a parent <Disclosure /> component.`);throw Error.captureStackTrace&&Error.captureStackTrace(r,St),r}return t}let Le=u.createContext(null);Le.displayName="DisclosurePanelContext";function zr(){return u.useContext(Le)}function Vr(e,t){return W(t.type,qr,e,t)}let Yr=u.Fragment;function Xr(e,t){let{defaultOpen:r=!1,...n}=e,a=u.useRef(null),s=z(t,Nr(y=>{a.current=y},e.as===void 0||e.as===u.Fragment)),i=u.useRef(null),o=u.useRef(null),c=u.useReducer(Vr,{disclosureState:r?0:1,linkedPanel:!1,buttonRef:o,panelRef:i,buttonId:null,panelId:null}),[{disclosureState:d,buttonId:l},p]=c,f=D(y=>{p({type:1});let b=bt(a);if(!b||!l)return;let h=y?y instanceof HTMLElement?y:y.current instanceof HTMLElement?y.current:b.getElementById(l):b.getElementById(l);h==null||h.focus()}),g=u.useMemo(()=>({close:f}),[f]),v=u.useMemo(()=>({open:d===0,close:f}),[d,f]),m={ref:s};return O.createElement(Fe.Provider,{value:c},O.createElement(De.Provider,{value:g},O.createElement(_r,{value:W(d,{0:oe.Open,1:oe.Closed})},G({ourProps:m,theirProps:n,slot:v,defaultTag:Yr,name:"Disclosure"}))))}let Zr="button";function Qr(e,t){let r=we(),{id:n=`headlessui-disclosure-button-${r}`,...a}=e,[s,i]=Me("Disclosure.Button"),o=zr(),c=o===null?!1:o===s.panelId,d=u.useRef(null),l=z(d,t,c?null:s.buttonRef),p=yt();u.useEffect(()=>{if(!c)return i({type:2,buttonId:n}),()=>{i({type:2,buttonId:null})}},[n,i,c]);let f=D(h=>{var P;if(c){if(s.disclosureState===1)return;switch(h.key){case k.Space:case k.Enter:h.preventDefault(),h.stopPropagation(),i({type:0}),(P=s.buttonRef.current)==null||P.focus();break}}else switch(h.key){case k.Space:case k.Enter:h.preventDefault(),h.stopPropagation(),i({type:0});break}}),g=D(h=>{switch(h.key){case k.Space:h.preventDefault();break}}),v=D(h=>{var P;Ur(h.currentTarget)||e.disabled||(c?(i({type:0}),(P=s.buttonRef.current)==null||P.focus()):i({type:0}))}),m=u.useMemo(()=>({open:s.disclosureState===0}),[s]),y=gt(e,d),b=c?{ref:l,type:y,onKeyDown:f,onClick:v}:{ref:l,id:n,type:y,"aria-expanded":s.disclosureState===0,"aria-controls":s.linkedPanel?s.panelId:void 0,onKeyDown:f,onKeyUp:g,onClick:v};return G({mergeRefs:p,ourProps:b,theirProps:a,slot:m,defaultTag:Zr,name:"Disclosure.Button"})}let Jr="div",en=ie.RenderStrategy|ie.Static;function tn(e,t){let r=we(),{id:n=`headlessui-disclosure-panel-${r}`,...a}=e,[s,i]=Me("Disclosure.Panel"),{close:o}=St("Disclosure.Panel"),c=yt(),d=z(t,s.panelRef,v=>{Br(()=>i({type:v?4:5}))});u.useEffect(()=>(i({type:3,panelId:n}),()=>{i({type:3,panelId:null})}),[n,i]);let l=jr(),p=l!==null?(l&oe.Open)===oe.Open:s.disclosureState===0,f=u.useMemo(()=>({open:s.disclosureState===0,close:o}),[s,o]),g={ref:d,id:n};return O.createElement(Le.Provider,{value:s.panelId},G({mergeRefs:c,ourProps:g,theirProps:a,slot:f,defaultTag:Jr,features:en,visible:p,name:"Disclosure.Panel"}))}let rn=K(Xr),nn=K(Qr),an=K(tn),Ln=Object.assign(rn,{Button:nn,Panel:an});function sn({onFocus:e}){let[t,r]=u.useState(!0),n=Hr();return t?O.createElement(Et,{as:"button",type:"button",features:wt.Focusable,onFocus:a=>{a.preventDefault();let s,i=50;function o(){if(i--<=0){s&&cancelAnimationFrame(s);return}if(e()){if(cancelAnimationFrame(s),!n.current)return;r(!1);return}s=requestAnimationFrame(o)}s=requestAnimationFrame(o)}}):null}const Pt=u.createContext(null);function on(){return{groups:new Map,get(e,t){var r;let n=this.groups.get(e);n||(n=new Map,this.groups.set(e,n));let a=(r=n.get(t))!=null?r:0;n.set(t,a+1);let s=Array.from(n.keys()).indexOf(t);function i(){let o=n.get(t);o>1?n.set(t,o-1):n.delete(t)}return[s,i]}}}function un({children:e}){let t=u.useRef(on());return u.createElement(Pt.Provider,{value:t},e)}function Tt(e){let t=u.useContext(Pt);if(!t)throw new Error("You must wrap your component in a <StableCollection>");let r=cn(),[n,a]=t.current.get(e,r);return u.useEffect(()=>a,[]),n}function cn(){var e,t,r;let n=(r=(t=(e=u.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED)==null?void 0:e.ReactCurrentOwner)==null?void 0:t.current)!=null?r:null;if(!n)return Symbol();let a=[],s=n;for(;s;)a.push(s.index),s=s.return;return"$."+a.join(".")}var ln=(e=>(e[e.Forwards=0]="Forwards",e[e.Backwards=1]="Backwards",e))(ln||{}),fn=(e=>(e[e.Less=-1]="Less",e[e.Equal=0]="Equal",e[e.Greater=1]="Greater",e))(fn||{}),dn=(e=>(e[e.SetSelectedIndex=0]="SetSelectedIndex",e[e.RegisterTab=1]="RegisterTab",e[e.UnregisterTab=2]="UnregisterTab",e[e.RegisterPanel=3]="RegisterPanel",e[e.UnregisterPanel=4]="UnregisterPanel",e))(dn||{});let pn={0(e,t){var r;let n=X(e.tabs,l=>l.current),a=X(e.panels,l=>l.current),s=n.filter(l=>{var p;return!((p=l.current)!=null&&p.hasAttribute("disabled"))}),i={...e,tabs:n,panels:a};if(t.index<0||t.index>n.length-1){let l=W(Math.sign(t.index-e.selectedIndex),{[-1]:()=>1,0:()=>W(Math.sign(t.index),{[-1]:()=>0,0:()=>0,1:()=>1}),1:()=>0});if(s.length===0)return i;let p=W(l,{0:()=>n.indexOf(s[0]),1:()=>n.indexOf(s[s.length-1])});return{...i,selectedIndex:p===-1?e.selectedIndex:p}}let o=n.slice(0,t.index),c=[...n.slice(t.index),...o].find(l=>s.includes(l));if(!c)return i;let d=(r=n.indexOf(c))!=null?r:e.selectedIndex;return d===-1&&(d=e.selectedIndex),{...i,selectedIndex:d}},1(e,t){var r;if(e.tabs.includes(t.tab))return e;let n=e.tabs[e.selectedIndex],a=X([...e.tabs,t.tab],i=>i.current),s=(r=a.indexOf(n))!=null?r:e.selectedIndex;return s===-1&&(s=e.selectedIndex),{...e,tabs:a,selectedIndex:s}},2(e,t){return{...e,tabs:e.tabs.filter(r=>r!==t.tab)}},3(e,t){return e.panels.includes(t.panel)?e:{...e,panels:X([...e.panels,t.panel],r=>r.current)}},4(e,t){return{...e,panels:e.panels.filter(r=>r!==t.panel)}}},je=u.createContext(null);je.displayName="TabsDataContext";function J(e){let t=u.useContext(je);if(t===null){let r=new Error(`<${e} /> is missing a parent <Tab.Group /> component.`);throw Error.captureStackTrace&&Error.captureStackTrace(r,J),r}return t}let _e=u.createContext(null);_e.displayName="TabsActionsContext";function Ue(e){let t=u.useContext(_e);if(t===null){let r=new Error(`<${e} /> is missing a parent <Tab.Group /> component.`);throw Error.captureStackTrace&&Error.captureStackTrace(r,Ue),r}return t}function hn(e,t){return W(t.type,pn,e,t)}let mn=u.Fragment;function bn(e,t){let{defaultIndex:r=0,vertical:n=!1,manual:a=!1,onChange:s,selectedIndex:i=null,...o}=e;const c=n?"vertical":"horizontal",d=a?"manual":"auto";let l=i!==null,p=z(t),[f,g]=u.useReducer(hn,{selectedIndex:i??r,tabs:[],panels:[]}),v=u.useMemo(()=>({selectedIndex:f.selectedIndex}),[f.selectedIndex]),m=me(s||(()=>{})),y=me(f.tabs),b=u.useMemo(()=>({orientation:c,activation:d,...f}),[c,d,f]),h=D(C=>(g({type:1,tab:C}),()=>g({type:2,tab:C}))),P=D(C=>(g({type:3,panel:C}),()=>g({type:4,panel:C}))),M=D(C=>{A.current!==C&&m.current(C),l||g({type:0,index:C})}),A=me(l?e.selectedIndex:f.selectedIndex),R=u.useMemo(()=>({registerTab:h,registerPanel:P,change:M}),[]);B(()=>{g({type:0,index:i??r})},[i]),B(()=>{if(A.current===void 0||f.tabs.length<=0)return;let C=X(f.tabs,q=>q.current);C.some((q,S)=>f.tabs[S]!==q)&&M(C.indexOf(f.tabs[A.current]))});let E={ref:p};return O.createElement(un,null,O.createElement(_e.Provider,{value:R},O.createElement(je.Provider,{value:b},b.tabs.length<=0&&O.createElement(sn,{onFocus:()=>{var C,q;for(let S of y.current)if(((C=S.current)==null?void 0:C.tabIndex)===0)return(q=S.current)==null||q.focus(),!0;return!1}}),G({ourProps:E,theirProps:o,slot:v,defaultTag:mn,name:"Tabs"}))))}let gn="div";function vn(e,t){let{orientation:r,selectedIndex:n}=J("Tab.List"),a=z(t);return G({ourProps:{ref:a,role:"tablist","aria-orientation":r},theirProps:e,slot:{selectedIndex:n},defaultTag:gn,name:"Tabs.List"})}let yn="button";function xn(e,t){var r,n;let a=we(),{id:s=`headlessui-tabs-tab-${a}`,...i}=e,{orientation:o,activation:c,selectedIndex:d,tabs:l,panels:p}=J("Tab"),f=Ue("Tab"),g=J("Tab"),v=u.useRef(null),m=z(v,t);B(()=>f.registerTab(v),[f,v]);let y=Tt("tabs"),b=l.indexOf(v);b===-1&&(b=y);let h=b===d,P=D(S=>{var H;let ce=S();if(ce===re.Success&&c==="auto"){let Ct=(H=bt(v))==null?void 0:H.activeElement,We=g.tabs.findIndex($t=>$t.current===Ct);We!==-1&&f.change(We)}return ce}),M=D(S=>{let H=l.map(ce=>ce.current).filter(Boolean);if(S.key===k.Space||S.key===k.Enter){S.preventDefault(),S.stopPropagation(),f.change(b);return}switch(S.key){case k.Home:case k.PageUp:return S.preventDefault(),S.stopPropagation(),P(()=>Y(H,L.First));case k.End:case k.PageDown:return S.preventDefault(),S.stopPropagation(),P(()=>Y(H,L.Last))}if(P(()=>W(o,{vertical(){return S.key===k.ArrowUp?Y(H,L.Previous|L.WrapAround):S.key===k.ArrowDown?Y(H,L.Next|L.WrapAround):re.Error},horizontal(){return S.key===k.ArrowLeft?Y(H,L.Previous|L.WrapAround):S.key===k.ArrowRight?Y(H,L.Next|L.WrapAround):re.Error}}))===re.Success)return S.preventDefault()}),A=u.useRef(!1),R=D(()=>{var S;A.current||(A.current=!0,(S=v.current)==null||S.focus({preventScroll:!0}),f.change(b),Sr(()=>{A.current=!1}))}),E=D(S=>{S.preventDefault()}),C=u.useMemo(()=>({selected:h}),[h]),q={ref:m,onKeyDown:M,onMouseDown:E,onClick:R,id:s,role:"tab",type:gt(e,v),"aria-controls":(n=(r=p[b])==null?void 0:r.current)==null?void 0:n.id,"aria-selected":h,tabIndex:h?0:-1};return G({ourProps:q,theirProps:i,slot:C,defaultTag:yn,name:"Tabs.Tab"})}let wn="div";function En(e,t){let{selectedIndex:r}=J("Tab.Panels"),n=z(t),a=u.useMemo(()=>({selectedIndex:r}),[r]);return G({ourProps:{ref:n},theirProps:e,slot:a,defaultTag:wn,name:"Tabs.Panels"})}let Sn="div",Pn=ie.RenderStrategy|ie.Static;function Tn(e,t){var r,n,a,s;let i=we(),{id:o=`headlessui-tabs-panel-${i}`,tabIndex:c=0,...d}=e,{selectedIndex:l,tabs:p,panels:f}=J("Tab.Panel"),g=Ue("Tab.Panel"),v=u.useRef(null),m=z(v,t);B(()=>g.registerPanel(v),[g,v]);let y=Tt("panels"),b=f.indexOf(v);b===-1&&(b=y);let h=b===l,P=u.useMemo(()=>({selected:h}),[h]),M={ref:m,id:o,role:"tabpanel","aria-labelledby":(n=(r=p[b])==null?void 0:r.current)==null?void 0:n.id,tabIndex:h?c:-1};return!h&&((a=d.unmount)==null||a)&&!((s=d.static)!=null&&s)?O.createElement(Et,{as:"span","aria-hidden":"true",...M}):G({ourProps:M,theirProps:d,slot:P,defaultTag:Sn,features:Pn,visible:h,name:"Tabs.Panel"})}let Cn=K(xn),$n=K(bn),In=K(vn),kn=K(En),An=K(Tn),jn=Object.assign(Cn,{Group:$n,List:In,Panels:kn,Panel:An});export{jn as $,Ln as A,Fn as G,mt as T,cr as a,mr as b,Mn as c,ur as g,lt as i,Nn as j,kt as m,ct as r,lr as u,ht as w};
