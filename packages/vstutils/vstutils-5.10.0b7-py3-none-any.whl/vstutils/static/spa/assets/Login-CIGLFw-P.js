import{r as c,E as g,n as f,f as y}from"./index-C9AoMnvk.js";import{u as b,a as w,b as F}from"./index-C-TOESMt.js";import{F as C}from"./FormGroup-CZPanTrh.js";const S={setup(){const o=c(!1),e=c(!1),t=b(),s=w(),n=c();async function r(a,i,p){try{return t.settings.extraTokenParams={second_factor:p},await t.signinResourceOwnerCredentials({username:a,password:i})}finally{t.settings.extraTokenParams={}}}let l="",u="";async function m(a,i,p){o.value=!0,n.value=void 0;try{await r(a,i,p),s()}catch(d){if(d instanceof g&&d.error==="invalid_request"){if(d.error_description==='Missing or invalid "second_factor" in request.')if(e.value){n.value="INVALID_CREDENTIALS";return}else{e.value=!0,l=a,u=i;return}n.value="INVALID_CREDENTIALS";return}console.error(d),n.value="OTHER_ERROR"}finally{o.value=!1}}function _(a,i){return m(a,i)}function v(a){return m(l,u,a)}return{login:_,provideSecondFactor:v,secondFactorRequired:e,isLoading:o,error:n}}};var x=function(){var e=this,t=e._self._c;return t("div",[e.secondFactorRequired?e._t("second-factor",null,{provideSecondFactor:e.provideSecondFactor,isLoading:e.isLoading,error:e.error}):e._t("default",null,{login:e.login,isLoading:e.isLoading,error:e.error})],2)},I=[],h=f(S,x,I,!1,null,null,null,null);const E=h.exports,L={components:{FormGroup:C,Oauth2ClientCredentialsGrantPageWrapper:E},setup(){const{i18n:o}=F(),e=y(()=>{const r=o.t("sign in to start your session");return r.slice(0,1).toUpperCase()+r.slice(1)}),t=c(""),s=c(""),n=c("");return{username:t,password:s,secondFactor:n,signInTo:e}}};var R=function(){var e=this,t=e._self._c;return t("Oauth2ClientCredentialsGrantPageWrapper",{scopedSlots:e._u([{key:"default",fn:function({login:s,error:n}){return[t("form",{on:{submit:function(r){return r.preventDefault(),(()=>s(e.username,e.password)).apply(null,arguments)}}},[t("p",{staticStyle:{"text-align":"center"}},[e._v(" "+e._s(e.signInTo)+" "+e._s(e.$t("or"))+" "),t("router-link",{attrs:{to:{name:"registration"}}},[e._v(e._s(e.$t("sign up")))]),e._v(". ")],1),t("div",{staticClass:"form-group has-feedback"},[t("input",{directives:[{name:"model",rawName:"v-model",value:e.username,expression:"username"}],staticClass:"form-control",attrs:{id:"username",autocomplete:"username",autofocus:"",maxlength:"254",name:"username",placeholder:e.$t("Username").toString(),required:"",type:"text"},domProps:{value:e.username},on:{input:function(r){r.target.composing||(e.username=r.target.value)}}})]),t("div",{staticClass:"form-group has-feedback"},[t("input",{directives:[{name:"model",rawName:"v-model",value:e.password,expression:"password"}],staticClass:"form-control",attrs:{id:"password",autocomplete:"current-password",name:"password",placeholder:e.$t("Password").toString(),type:"password",required:""},domProps:{value:e.password},on:{input:function(r){r.target.composing||(e.password=r.target.value)}}})]),n?t("div",{staticClass:"alert alert-danger",attrs:{role:"alert"}},[e._v(" "+e._s(n==="INVALID_CREDENTIALS"?e.$t("Invalid username or password"):e.$t("Error! Try again later"))+" ")]):e._e(),t("button",{staticClass:"btn btn-primary btn-block",staticStyle:{"margin-bottom":"5px","text-transform":"capitalize"},attrs:{type:"submit"}},[e._v(" "+e._s(e.$t("sign in"))+" ")]),t("router-link",{staticStyle:{"text-transform":"capitalize"},attrs:{to:{name:"password-reset"}}},[e._v(" "+e._s(e.$t("forgot password"))+"? ")])],1)]}},{key:"second-factor",fn:function({provideSecondFactor:s,error:n}){return[t("form",{on:{submit:function(r){return r.preventDefault(),(()=>s(e.secondFactor)).apply(null,arguments)}}},[t("FormGroup",{attrs:{label:"Authentication code"},scopedSlots:e._u([{key:"default",fn:function({id:r,classes:l}){return[t("input",{directives:[{name:"model",rawName:"v-model",value:e.secondFactor,expression:"secondFactor"}],class:l,attrs:{id:r,type:"text",inputmode:"numeric"},domProps:{value:e.secondFactor},on:{input:function(u){u.target.composing||(e.secondFactor=u.target.value)}}})]}}],null,!0)}),t("p",[e._v(" "+e._s(e.$t("Enter the code from the two-factor app on your mobile device. If you've lost your device, you may enter one of your recovery codes."))+" ")]),n?t("div",{staticClass:"alert alert-danger",attrs:{role:"alert"}},[e._v(" "+e._s(n==="INVALID_CREDENTIALS"?"Invalid code":"Error! Try again later")+" ")]):e._e(),t("button",{staticClass:"btn btn-primary btn-block",staticStyle:{"margin-bottom":"5px","text-transform":"capitalize"},attrs:{type:"submit"}},[e._v(" "+e._s(e.$t("sign in"))+" ")])],1)]}}])})},T=[],$=f(L,R,T,!1,null,null,null,null);const D=$.exports;export{D as default};