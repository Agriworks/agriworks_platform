(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-87dfcb22"],{4863:function(t,e,n){"use strict";n.r(e);var i=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("h1",[t._v("Merge Datasets")]),this.datasets.length>0?n("div",{staticClass:".grid-container"},t._l(t.datasets,(function(e){return n("div",{key:e.id,staticClass:"datasetCheckbox"},[n("v-checkbox",{attrs:{label:e.name,value:e.id},model:{value:t.selectedDatasets,callback:function(e){t.selectedDatasets=e},expression:"selectedDatasets"}})],1)})),0):t._e(),n("v-btn",{staticClass:"submitButton",attrs:{"x-large":"",color:"success",dark:""},on:{click:t.selectColumns}},[t._v("\n    Next\n  ")])],1)},s=[],c={name:"Merge",data:function(){return{selectedDatasets:[]}},computed:{datasets:function(){return this.$store.state.datasets}},methods:{selectColumns:function(){}},mounted:function(){this.$store.dispatch("fetchDatasets"),console.log(this.datasets)}},a=c,r=(n("c7ad"),n("2877")),o=n("6544"),u=n.n(o),d=n("8336"),h=(n("8e6e"),n("ac6a"),n("456d"),n("6b54"),n("bd86")),l=(n("6ca7"),n("ec29"),n("9d26")),p=n("c37a"),f=n("fe09");function m(t,e){var n=Object.keys(t);if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(t);e&&(i=i.filter((function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable}))),n.push.apply(n,i)}return n}function b(t){for(var e=1;e<arguments.length;e++){var n=null!=arguments[e]?arguments[e]:{};e%2?m(Object(n),!0).forEach((function(e){Object(h["a"])(t,e,n[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(n)):m(Object(n)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(n,e))}))}return t}var v=f["a"].extend({name:"v-checkbox",props:{indeterminate:Boolean,indeterminateIcon:{type:String,default:"$checkboxIndeterminate"},offIcon:{type:String,default:"$checkboxOff"},onIcon:{type:String,default:"$checkboxOn"}},data:function(){return{inputIndeterminate:this.indeterminate}},computed:{classes:function(){return b({},p["a"].options.computed.classes.call(this),{"v-input--selection-controls":!0,"v-input--checkbox":!0,"v-input--indeterminate":this.inputIndeterminate})},computedIcon:function(){return this.inputIndeterminate?this.indeterminateIcon:this.isActive?this.onIcon:this.offIcon},validationState:function(){if(!this.disabled||this.inputIndeterminate)return this.hasError&&this.shouldValidate?"error":this.hasSuccess?"success":null!==this.hasColor?this.computedColor:void 0}},watch:{indeterminate:function(t){var e=this;this.$nextTick((function(){return e.inputIndeterminate=t}))},inputIndeterminate:function(t){this.$emit("update:indeterminate",t)},isActive:function(){this.indeterminate&&(this.inputIndeterminate=!1)}},methods:{genCheckbox:function(){return this.$createElement("div",{staticClass:"v-input--selection-controls__input"},[this.$createElement(l["a"],this.setTextColor(this.validationState,{props:{dense:this.dense,dark:this.dark,light:this.light}}),this.computedIcon),this.genInput("checkbox",b({},this.attrs$,{"aria-checked":this.inputIndeterminate?"mixed":this.isActive.toString()})),this.genRipple(this.setTextColor(this.rippleState))])},genDefaultSlot:function(){return[this.genCheckbox(),this.genLabel()]}}}),g=Object(r["a"])(a,i,s,!1,null,"6825277a",null);e["default"]=g.exports;u()(g,{VBtn:d["a"],VCheckbox:v})},"6ca7":function(t,e,n){},"981e":function(t,e,n){},c7ad:function(t,e,n){"use strict";var i=n("981e"),s=n.n(i);s.a}}]);
//# sourceMappingURL=chunk-87dfcb22.02647224.js.map