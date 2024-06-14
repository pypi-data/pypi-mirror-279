import{n as a,B as o,b as i}from"./index-C9AoMnvk.js";const r={name:"NestedDeletionModal",components:{BootstrapModal:o},data(){return{view:void 0,action:void 0}},methods:{execute({instances:e,action:t}){this.instances=e,this.action=t,this.openModal()},closeModal(){this.$refs.modal.close()},openModal(){this.$refs.modal.open()},async performDeletion(e){if(this.closeModal(),this.$app.store.page.view.type===i.PAGE){await this.$app.store.page.removeInstance({instance:this.$app.store.page.instance,purge:e});return}if(this.instances.length===1){await this.$app.store.page.removeInstance({action:this.action,instance:this.instances.pop(),fromList:!0,purge:e});return}await this.$app.store.page.removeInstances({action:this.action,instances:this.instances,purge:e})}}};var l=function(){var t=this,n=t._self._c;return n("BootstrapModal",{ref:"modal",attrs:{title:t.$t("Select an action for this instances")},scopedSlots:t._u([{key:"body",fn:function(){return[n("div",{staticClass:"my-2 d-flex justify-content-center align-items-center"},[n("ul",{staticClass:"list-group list-group-flush"},t._l(t.instances,function(s){return n("li",{key:s.getPkValue(),staticClass:"list-group-item"},[t._v(" "+t._s(s.getViewFieldValue())+" ")])}),0)])]},proxy:!0},{key:"footer",fn:function(){return[n("button",{staticClass:"btn btn-primary",attrs:{"aria-label":"Cancel"},on:{click:function(s){return t.performDeletion(!1)}}},[t._v(" "+t._s(t.$t("Remove from list"))+" ")]),n("button",{staticClass:"btn btn-danger",attrs:{"aria-label":"Cancel"},on:{click:function(s){return t.performDeletion(!0)}}},[t._v(" "+t._s(t.$t("Purge"))+" ")])]},proxy:!0},{key:"activator",fn:function(){return[t._t("default",null,{execute:t.execute})]},proxy:!0}],null,!0)})},c=[],u=a(r,l,c,!1,null,null,null,null);const f=u.exports;export{f as default};