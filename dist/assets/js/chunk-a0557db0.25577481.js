(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-a0557db0"],{"20f6":function(s,r,e){},"2fa4":function(s,r,e){"use strict";e("20f6");var t=e("80d2");r["a"]=Object(t["h"])("spacer","div","v-spacer")},"4bd4":function(s,r,e){"use strict";e("8e6e"),e("456d");var t=e("bd86"),i=(e("7514"),e("ac6a"),e("8615"),e("6762"),e("2fdb"),e("58df")),o=e("7e2b"),a=e("3206");function n(s,r){var e=Object.keys(s);if(Object.getOwnPropertySymbols){var t=Object.getOwnPropertySymbols(s);r&&(t=t.filter((function(r){return Object.getOwnPropertyDescriptor(s,r).enumerable}))),e.push.apply(e,t)}return e}function d(s){for(var r=1;r<arguments.length;r++){var e=null!=arguments[r]?arguments[r]:{};r%2?n(Object(e),!0).forEach((function(r){Object(t["a"])(s,r,e[r])})):Object.getOwnPropertyDescriptors?Object.defineProperties(s,Object.getOwnPropertyDescriptors(e)):n(Object(e)).forEach((function(r){Object.defineProperty(s,r,Object.getOwnPropertyDescriptor(e,r))}))}return s}r["a"]=Object(i["a"])(o["a"],Object(a["b"])("form")).extend({name:"v-form",inheritAttrs:!1,props:{lazyValidation:Boolean,value:Boolean},data:function(){return{inputs:[],watchers:[],errorBag:{}}},watch:{errorBag:{handler:function(s){var r=Object.values(s).includes(!0);this.$emit("input",!r)},deep:!0,immediate:!0}},methods:{watchInput:function(s){var r=this,e=function(s){return s.$watch("hasError",(function(e){r.$set(r.errorBag,s._uid,e)}),{immediate:!0})},t={_uid:s._uid,valid:function(){},shouldValidate:function(){}};return this.lazyValidation?t.shouldValidate=s.$watch("shouldValidate",(function(i){i&&(r.errorBag.hasOwnProperty(s._uid)||(t.valid=e(s)))})):t.valid=e(s),t},validate:function(){return 0===this.inputs.filter((function(s){return!s.validate(!0)})).length},reset:function(){this.inputs.forEach((function(s){return s.reset()})),this.resetErrorBag()},resetErrorBag:function(){var s=this;this.lazyValidation&&setTimeout((function(){s.errorBag={}}),0)},resetValidation:function(){this.inputs.forEach((function(s){return s.resetValidation()})),this.resetErrorBag()},register:function(s){this.inputs.push(s),this.watchers.push(this.watchInput(s))},unregister:function(s){var r=this.inputs.find((function(r){return r._uid===s._uid}));if(r){var e=this.watchers.find((function(s){return s._uid===r._uid}));e&&(e.valid(),e.shouldValidate()),this.watchers=this.watchers.filter((function(s){return s._uid!==r._uid})),this.inputs=this.inputs.filter((function(s){return s._uid!==r._uid})),this.$delete(this.errorBag,r._uid)}}},render:function(s){var r=this;return s("form",{staticClass:"v-form",attrs:d({novalidate:!0},this.attrs$),on:{submit:function(s){return r.$emit("submit",s)}}},this.$slots.default)}})},"77be":function(s,r,e){"use strict";e.r(r);var t=function(){var s=this,r=s.$createElement,e=s._self._c||r;return e("div",[e("div",{staticClass:"main"},[e("div",{staticClass:"container"},[s._m(0),e("v-card",{staticClass:"shadow rounded"},[e("div",{staticClass:"card-body"},[e("div",{staticClass:"row"},[e("div",{staticClass:"col-auto"},[e("strong",[s._v("Email Address: ")])]),e("div",{staticClass:"col"},[e("span",[s._v(" "+s._s(s.email)+" ")])]),e("div",{staticClass:"col text-right"},[e("v-dialog",{attrs:{width:"500"},scopedSlots:s._u([{key:"activator",fn:function(r){var t=r.on;return[e("v-btn",s._g({attrs:{color:"green",dark:""}},t),[s._v("\n                  Change\n                ")])]}}]),model:{value:s.forms.email.show,callback:function(r){s.$set(s.forms.email,"show",r)},expression:"forms.email.show"}},[e("v-card",[e("v-card-title",{staticClass:"headline",attrs:{"primary-title":""}},[s._v("\n                  Change Email\n                ")]),e("v-card-text",[e("v-form",{ref:"changeEmailForm",staticClass:"form-signin"},[e("div",{staticClass:"form-label-group"},[e("v-text-field",{ref:"emailPassword",attrs:{id:"inputCurrentPassword",label:"Current Password",required:"",autofocus:"",rules:s.forms.email.fields.password.rules,"append-icon":s.forms.email.fields.password.visibility?"visibility":"visibility_off",type:s.forms.email.fields.password.visibility?"text":"password",color:"green",error:s.forms.email.fields.password.state,"error-messages":s.forms.email.fields.password.error},on:{"click:append":function(){return s.forms.email.fields.password.visibility=!s.forms.email.fields.password.visibility}},model:{value:s.forms.email.fields.password.input,callback:function(r){s.$set(s.forms.email.fields.password,"input",r)},expression:"forms.email.fields.password.input"}}),e("v-text-field",{ref:"emailEmail",attrs:{type:"email",id:"inputEmail",label:"New Email",required:"",rules:s.forms.email.fields.email.rules,color:"green",error:s.forms.email.fields.email.state,"error-messages":s.forms.email.fields.email.error},model:{value:s.forms.email.fields.email.input,callback:function(r){s.$set(s.forms.email.fields.email,"input",r)},expression:"forms.email.fields.email.input"}})],1)])],1),e("v-card-actions",[e("v-spacer"),e("v-btn",{attrs:{color:"green",text:""},on:{click:function(r){s.forms.email.show=!1}}},[s._v("Close")]),e("v-btn",{attrs:{color:"green",text:""},on:{click:s.submitEmail}},[s._v("Save")])],1)],1)],1)],1)]),e("div",{staticClass:"row"},[e("div",{staticClass:"col-auto"},[e("strong",[s._v("Password:        ")])]),e("div",{staticClass:"col"}),e("div",{staticClass:"col text-right"},[e("v-dialog",{attrs:{width:"500"},scopedSlots:s._u([{key:"activator",fn:function(r){var t=r.on;return[e("v-btn",s._g({attrs:{color:"green",dark:""}},t),[s._v("\n                  Change\n                ")])]}}]),model:{value:s.forms.password.show,callback:function(r){s.$set(s.forms.password,"show",r)},expression:"forms.password.show"}},[e("v-card",[e("v-card-title",{staticClass:"headline",attrs:{"primary-title":""}},[s._v("\n                  Change Password\n                ")]),e("v-card-text",[e("v-form",{ref:"changePasswordForm",staticClass:"form-signin"},[e("div",{staticClass:"form-label-group"},[e("v-text-field",{ref:"passwordCurrent",attrs:{id:"inputCurrentPassword",label:"Current Password",required:"",autofocus:"",rules:s.forms.password.fields.currentPassword.rules,"append-icon":s.forms.password.fields.currentPassword.visibility?"visibility":"visibility_off",type:s.forms.password.fields.currentPassword.visibility?"text":"password",color:"green",error:s.forms.password.fields.currentPassword.state,"error-messages":s.forms.password.fields.currentPassword.error},on:{"click:append":function(){return s.forms.password.fields.currentPassword.visibility=!s.forms.password.fields.currentPassword.visibility}},model:{value:s.forms.password.fields.currentPassword.input,callback:function(r){s.$set(s.forms.password.fields.currentPassword,"input",r)},expression:"forms.password.fields.currentPassword.input"}}),e("v-text-field",{ref:"passwordNewPassword",attrs:{id:"inputPassword",label:"New Password",required:"",rules:s.forms.password.fields.newPassword.rules,"append-icon":s.forms.password.fields.newPassword.visibility?"visibility":"visibility_off",type:s.forms.password.fields.newPassword.visibility?"text":"password",color:"green",error:s.forms.password.fields.newPassword.state,"error-messages":s.forms.password.fields.newPassword.error},on:{"click:append":function(){return s.forms.password.fields.newPassword.visibility=!s.forms.password.fields.newPassword.visibility}},model:{value:s.forms.password.fields.newPassword.input,callback:function(r){s.$set(s.forms.password.fields.newPassword,"input",r)},expression:"forms.password.fields.newPassword.input"}}),e("v-text-field",{ref:"passwordConfirmPassword",attrs:{id:"inputConfirmPassword",label:"Confirm New Password",required:"",rules:s.forms.password.fields.confirmNewPassword.rules,"append-icon":s.forms.password.fields.confirmNewPassword.visibility?"visibility":"visibility_off",type:s.forms.password.fields.confirmNewPassword.visibility?"text":"password",color:"green",error:s.forms.password.fields.confirmNewPassword.state,"error-messages":s.forms.password.fields.confirmNewPassword.error},on:{"click:append":function(){return s.forms.password.fields.confirmNewPassword.visibility=!s.forms.password.fields.confirmNewPassword.visibility}},model:{value:s.forms.password.fields.confirmNewPassword.input,callback:function(r){s.$set(s.forms.password.fields.confirmNewPassword,"input",r)},expression:"forms.password.fields.confirmNewPassword.input"}})],1)])],1),e("v-card-actions",[e("v-spacer"),e("v-btn",{attrs:{color:"green",text:""},on:{click:function(r){s.forms.password.show=!1}}},[s._v("Close")]),e("v-btn",{attrs:{color:"green",text:""},on:{click:s.submitPassword}},[s._v("Save")])],1)],1)],1)],1)]),e("div",{staticClass:"row"},[e("div",{staticClass:"text-xs-center"},[e("v-dialog",{attrs:{width:"500"},scopedSlots:s._u([{key:"activator",fn:function(r){var t=r.on;return[e("v-btn",s._g({attrs:{color:"red",dark:""}},t),[s._v("\n                  Delete Account\n                ")])]}}]),model:{value:s.deleteAccountConfirmation,callback:function(r){s.deleteAccountConfirmation=r},expression:"deleteAccountConfirmation"}},[e("v-card",[e("v-card-title",{staticClass:"headline",attrs:{"primary-title":""}},[s._v("\n                  Are you sure?\n                ")]),e("v-card-text",[s._v("\n                  Deleting your account will also delete your datasets.\n\n                ")]),e("v-card-actions",[e("v-spacer"),e("v-btn",{attrs:{color:"grey",text:""},on:{click:function(r){s.deleteAccountConfirmation=!1}}},[s._v("Close")]),e("v-btn",{attrs:{color:"red",text:""},on:{click:s.deleteAccount}},[s._v("Delete Account")])],1)],1)],1)],1)])])])],1)])])},i=[function(){var s=this,r=s.$createElement,e=s._self._c||r;return e("div",{staticClass:"row"},[e("h1",{attrs:{align:"center"}},[s._v("Account settings")])])}],o=(e("d1e7"),e("d722")),a={computed:{email:function(){return this.$store.state.user}},data:function(){return{deleteAccountConfirmation:!1,forms:{email:{show:!1,fields:{password:{input:"",visibility:!1,state:!1,error:[],rules:[function(s){return!!s||"Password is required"}]},email:{input:"",state:!1,error:[],rules:[function(s){return!!s||"E-mail is required"},function(s){return/.+@.+/.test(s)||"E-mail must be valid"}]}}},password:{show:!1,fields:{currentPassword:{input:"",visibility:!1,state:!1,error:[],rules:[function(s){return!!s||"Password is required"}]},newPassword:{input:"",visibility:!1,state:!1,error:[],rules:[function(s){return!!s||"Password is required"}]},confirmNewPassword:{input:"",visibility:!1,state:!1,error:[],rules:[function(s){return!!s||"Confirm Password is required"}]}}}}}},methods:{submitEmail:function(){var s=!1;if(1==this.forms.email.fields.password.error.length){var r=this.forms.email.fields.password.error.pop();"Incorrect Password"==r?(s=!0,this.forms.email.fields.password.state=!1):this.forms.email.fields.password.error.push(r)}var e=!1;if(1==this.forms.email.fields.email.error.length){var t=this.forms.email.fields.email.error.pop();"There is already exists an account with this email"==t?(e=!0,this.forms.email.fields.email.state=!1,this.$refs["emailEmail"].resetValidation()):this.forms.email.fields.email.error.push(t)}this.$refs["emailPassword"].hasError&&!s||this.$refs["emailEmail"].hasError&&!e||o["a"].updateEmail(this)},submitPassword:function(){var s=!1;if(1==this.forms.password.fields.currentPassword.error.length){var r=this.forms.password.fields.currentPassword.error.pop();"Incorrect Password"==r?(this.forms.password.fields.currentPassword.state=!1,s=!0):this.forms.password.fields.currentPassword.error.push(r)}var e=!1;if(1==this.forms.password.fields.confirmNewPassword.error.length){var t=this.forms.password.fields.confirmNewPassword.error.pop();"Confirm password does not match the new password"==t?(this.forms.password.fields.confirmNewPassword.state=!1,e=!0):this.forms.password.fields.confirmNewPassword.error.push(t)}this.$refs["passwordCurrent"].hasError&&!s||this.$refs["passwordNewPassword"].hasError||this.$refs["passwordConfirmPassword"].hasError&&!e||(this.forms.password.fields.newPassword.input!=this.forms.password.fields.confirmNewPassword.input?(this.forms.password.fields.confirmNewPassword.state=!0,this.forms.password.fields.confirmNewPassword.error.push("Confirm password does not match the new password")):o["a"].updatePassword(this))},deleteAccount:function(){o["a"].deleteAccount()}}},n=a,d=(e("7893"),e("2877")),l=e("6544"),c=e.n(l),f=e("8336"),u=e("b0af"),w=e("99d9"),m=e("169a"),p=e("4bd4"),v=e("2fa4"),h=e("8654"),b=Object(d["a"])(n,t,i,!1,null,"287b1fbc",null);r["default"]=b.exports;c()(b,{VBtn:f["a"],VCard:u["a"],VCardActions:w["a"],VCardText:w["b"],VCardTitle:w["c"],VDialog:m["a"],VForm:p["a"],VSpacer:v["a"],VTextField:h["a"]})},7893:function(s,r,e){"use strict";var t=e("e28d"),i=e.n(t);i.a},"99d9":function(s,r,e){"use strict";e.d(r,"a",(function(){return o})),e.d(r,"b",(function(){return n})),e.d(r,"c",(function(){return d}));var t=e("b0af"),i=e("80d2"),o=Object(i["h"])("v-card__actions"),a=Object(i["h"])("v-card__subtitle"),n=Object(i["h"])("v-card__text"),d=Object(i["h"])("v-card__title");t["a"]},d1e7:function(s,r,e){},e28d:function(s,r,e){}}]);
//# sourceMappingURL=chunk-a0557db0.25577481.js.map