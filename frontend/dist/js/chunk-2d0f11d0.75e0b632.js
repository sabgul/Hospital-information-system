(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d0f11d0"],{"9ef4":function(e,t,n){"use strict";n.r(t);var a=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[e._m(0),n("div",{staticClass:"main__content"},[n("h5",[e._v(" Patients overview ")]),n("br"),n("patients-table",{attrs:{patients:e.patients}})],1)])},i=[function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"main__content"},[n("h1",[e._v("All patients")]),n("br"),n("p",[e._v(" This module provides you with an overview of all your patients. More information can be obtained by clicking on the name of patient, which leads to their profile. "),n("br"),e._v(" There you can see detailed description of their health concerns, as well as their personal information. ")])])}],r=(n("96cf"),n("1da1")),o=n("5530"),s=n("1813"),c=n("184d"),l=n("2f62"),u={name:"PatientsOverview",components:{PatientsTable:c["a"]},computed:Object(o["a"])({},Object(l["b"])(["user","userRole"])),data:function(){return{patients:[],page:1,max:10,searchValue:""}},created:function(){var e=this;return Object(r["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:"admin"===e.userRole&&s["a"].getAll().then((function(t){e.patients=t.data})),"doctor"===e.userRole&&s["a"].getAllByDoctor(e.user.id).then((function(t){e.patients=t.data}));case 2:case"end":return t.stop()}}),t)})))()}},d=u,p=n("0c7c"),h=Object(p["a"])(d,a,i,!1,null,null,null);t["default"]=h.exports}}]);
//# sourceMappingURL=chunk-2d0f11d0.75e0b632.js.map