import{e as c,r,f,B as p,M as d,j as _,m,n as v}from"./index-C9AoMnvk.js";const b=c({__name:"FiltersModalDetail",props:{view:null},setup(o){const e=o,l=r(null),t=_(),a=t.store.page,s=f(()=>e.view.filtersModelClass),n=r();function i(){l.value.open(),n.value=new s.value(m({},a.filters??{}))}function u(){a.applyFilters(n.value.sandbox.value),l.value.close()}return{__sfc:!0,props:e,modalRef:l,app:t,store:a,model:s,instance:n,openModal:i,filter:u,BootstrapModal:p,ModelFields:d}}});var y=function(){var e=this,l=e._self._c,t=e._self._setupProxy;return t.model?l(t.BootstrapModal,{ref:"modalRef",attrs:{title:e.$u.capitalize(e.$ts("filters"))},scopedSlots:e._u([{key:"default",fn:function(){return[t.instance?l(t.ModelFields,{attrs:{model:t.model,data:t.instance.sandbox.value,editable:"","flat-if-possible":"","flat-fields-classes":"col-12"},on:{"set-value":a=>{var s;return(s=t.instance)==null?void 0:s.sandbox.set(a)}}}):e._e()]},proxy:!0},{key:"footer",fn:function({closeModal:a}){return[l("button",{staticClass:"btn btn-default btn-close-filters-modal",attrs:{"aria-label":"Cancel"},on:{click:a}},[e._v(" "+e._s(e.$u.capitalize(e.$ts("cancel")))+" ")]),l("button",{staticClass:"btn btn-primary btn-apply-filters",attrs:{"aria-label":"Filter"},on:{click:t.filter}},[e._v(" "+e._s(e.$u.capitalize(e.$ts("apply")))+" ")])]}},{key:"activator",fn:function(){return[e._t("default",null,{execute:t.openModal})]},proxy:!0}],null,!0)}):e._e()},M=[],x=v(b,y,M,!1,null,null,null,null);const $=x.exports;export{$ as default};