export const API_BASE = import.meta.env.VITE_API_BASE_URL || '';
export const RISK_BANDS = [{label:'Low',min:0,max:24,color:'#18a579'},{label:'Moderate',min:25,max:49,color:'#e5b93f'},{label:'High',min:50,max:74,color:'#ef8b3d'},{label:'Critical',min:75,max:100,color:'#dc5555'}];
export const AREAS = [
 {name:'Chattogram',lat:22.3569,lng:91.7832,risk:63,cases:118,division:'Chattogram'},
 {name:'Cox’s Bazar',lat:21.4272,lng:92.0058,risk:44,cases:54,division:'Chattogram'},
 {name:'Cumilla',lat:23.4607,lng:91.1809,risk:51,cases:77,division:'Chattogram'},
 {name:'Feni',lat:23.0159,lng:91.3976,risk:35,cases:32,division:'Chattogram'},
 {name:'Dhaka',lat:23.8103,lng:90.4125,risk:72,cases:230,division:'Dhaka'},
 {name:'Khulna',lat:22.8456,lng:89.5403,risk:31,cases:28,division:'Khulna'},
 {name:'Rajshahi',lat:24.3745,lng:88.6042,risk:22,cases:16,division:'Rajshahi'},
 {name:'Sylhet',lat:24.8949,lng:91.8687,risk:47,cases:49,division:'Sylhet'},
 {name:'Barishal',lat:22.7010,lng:90.3535,risk:39,cases:36,division:'Barishal'},
 {name:'Rangpur',lat:25.7439,lng:89.2752,risk:19,cases:12,division:'Rangpur'},
 {name:'Mymensingh',lat:24.7471,lng:90.4203,risk:29,cases:22,division:'Mymensingh'}
];
export const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
