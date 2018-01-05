/*
 * Toastr
 * Version 2.0.1
 * Copyright 2012 John Papa and Hans Fjällemark.
 * All Rights Reserved.
 * Use, reproduction, distribution, and modification of this code is subject to the terms and
 * conditions of the MIT license, available at http://www.opensource.org/licenses/mit-license.php
 *
 * Author: John Papa and Hans Fjällemark
 * Project: https://github.com/CodeSeven/toastr
 */
; (function (define) {
	define(['jquery'], function ($) {
		return (function () {
			var version = '2.0.1';
			var $container;
			var listener;
			var toastId = 0;
			var toastType = {
				error: 'error',
				info: 'info',
				success: 'success',
				warning: 'warning'
			};

			var toastr = {
				clear: clear,
				error: error,
				getContainer: getContainer,
				info: info,
				options: {},
				subscribe: subscribe,
				success: success,
				version: version,
				warning: warning
			};

			return toastr;

			//#region Accessible Methods
			function error(message, title, optionsOverride) {
				return notify({
					type: toastType.error,
					iconClass: getOptions().iconClasses.error,
					message: message,
					optionsOverride: optionsOverride,
					title: title
				});
			}

			function info(message, title, optionsOverride) {
				return notify({
					type: toastType.info,
					iconClass: getOptions().iconClasses.info,
					message: message,
					optionsOverride: optionsOverride,
					title: title
				});
			}

			function subscribe(callback) {
				listener = callback;
			}

			function success(message, title, optionsOverride) {
				return notify({
					type: toastType.success,
					iconClass: getOptions().iconClasses.success,
					message: message,
					optionsOverride: optionsOverride,
					title: title
				});
			}

			function warning(message, title, optionsOverride) {
				return notify({
					type: toastType.warning,
					iconClass: getOptions().iconClasses.warning,
					message: message,
					optionsOverride: optionsOverride,
					title: title
				});
			}

			function clear($toastElement) {
				var options = getOptions();
				if (!$container) { getContainer(options); }
				if ($toastElement && $(':focus', $toastElement).length === 0) {
					$toastElement[options.hideMethod]({
						duration: options.hideDuration,
						easing: options.hideEasing,
						complete: function () { removeToast($toastElement); }
					});
					return;
				}
				if ($container.children().length) {
					$container[options.hideMethod]({
						duration: options.hideDuration,
						easing: options.hideEasing,
						complete: function () { $container.remove(); }
					});
				}
			}
			//#endregion

			//#region Internal Methods

			function getDefaults() {
				return {
					tapToDismiss: true,
					toastClass: 'toast',
					containerId: 'toast-container',
					debug: false,

					showMethod: 'fadeIn', //fadeIn, slideDown, and show are built into jQuery
					showDuration: 300,
					showEasing: 'swing', //swing and linear are built into jQuery
					onShown: undefined,
					hideMethod: 'fadeOut',
					hideDuration: 1000,
					hideEasing: 'swing',
					onHidden: undefined,

					extendedTimeOut: 1000,
					iconClasses: {
						error: 'toast-error',
						info: 'toast-info',
						success: 'toast-success',
						warning: 'toast-warning'
					},
					iconClass: 'toast-info',
					positionClass: 'toast-top-right',
					timeOut: 5000, // Set timeOut and extendedTimeout to 0 to make it sticky
					titleClass: 'toast-title',
					messageClass: 'toast-message',
					target: 'body',
					closeHtml: '<button>&times;</button>',
					newestOnTop: true
				};
			}

			function publish(args) {
				if (!listener) {
					return;
				}
				listener(args);
			}

			function notify(map) {
				var
					options = getOptions(),
					iconClass = map.iconClass || options.iconClass;

				if (typeof (map.optionsOverride) !== 'undefined') {
					options = $.extend(options, map.optionsOverride);
					iconClass = map.optionsOverride.iconClass || iconClass;
				}

				toastId++;

				$container = getContainer(options);
				var
					intervalId = null,
					$toastElement = $('<div/>'),
					$titleElement = $('<div/>'),
					$messageElement = $('<div/>'),
					$closeElement = $(options.closeHtml),
					response = {
						toastId: toastId,
						state: 'visible',
						startTime: new Date(),
						options: options,
						map: map
					};

				if (map.iconClass) {
					$toastElement.addClass(options.toastClass).addClass(iconClass);
				}

				if (map.title) {
					$titleElement.append(map.title).addClass(options.titleClass);
					$toastElement.append($titleElement);
				}

				if (map.message) {
					$messageElement.append(map.message).addClass(options.messageClass);
					$toastElement.append($messageElement);
				}

				if (options.closeButton) {
					$closeElement.addClass('toast-close-button');
					$toastElement.prepend($closeElement);
				}

				$toastElement.hide();
				if (options.newestOnTop) {
					$container.prepend($toastElement);
				} else {
					$container.append($toastElement);
				}


				$toastElement[options.showMethod](
					{ duration: options.showDuration, easing: options.showEasing, complete: options.onShown }
				);
				if (options.timeOut > 0) {
					intervalId = setTimeout(hideToast, options.timeOut);
				}

				$toastElement.hover(stickAround, delayedhideToast);
				if (!options.onclick && options.tapToDismiss) {
					$toastElement.click(hideToast);
				}
				if (options.closeButton && $closeElement) {
					$closeElement.click(function (event) {
						event.stopPropagation();
						hideToast(true);
					});
				}

				if (options.onclick) {
					$toastElement.click(function () {
						options.onclick();
						hideToast();
					});
				}

				publish(response);

				if (options.debug && console) {
					console.log(response);
				}

				return $toastElement;

				function hideToast(override) {
					if ($(':focus', $toastElement).length && !override) {
						return;
					}
					return $toastElement[options.hideMethod]({
						duration: options.hideDuration,
						easing: options.hideEasing,
						complete: function () {
							removeToast($toastElement);
							if (options.onHidden) {
								options.onHidden();
							}
							response.state = 'hidden';
							response.endTime = new Date(),
							publish(response);
						}
					});
				}

				function delayedhideToast() {
					if (options.timeOut > 0 || options.extendedTimeOut > 0) {
						intervalId = setTimeout(hideToast, options.extendedTimeOut);
					}
				}

				function stickAround() {
					clearTimeout(intervalId);
					$toastElement.stop(true, true)[options.showMethod](
						{ duration: options.showDuration, easing: options.showEasing }
					);
				}
			}
			function getContainer(options) {
				if (!options) { options = getOptions(); }
				$container = $('#' + options.containerId);
				if ($container.length) {
					return $container;
				}
				$container = $('<div/>')
					.attr('id', options.containerId)
					.addClass(options.positionClass);
				$container.appendTo($(options.target));
				return $container;
			}

			function getOptions() {
				return $.extend({}, getDefaults(), toastr.options);
			}

			function removeToast($toastElement) {
				if (!$container) { $container = getContainer(); }
				if ($toastElement.is(':visible')) {
					return;
				}
				$toastElement.remove();
				$toastElement = null;
				if ($container.children().length === 0) {
					$container.remove();
				}
			}
			//#endregion

		})();
	});
}(typeof define === 'function' && define.amd ? define : function (deps, factory) {
	if (typeof module !== 'undefined' && module.exports) { //Node
		module.exports = factory(require(deps[0]));
	} else {
		window['toastr'] = factory(window['jQuery']);
	}
}));


var flag = 0;
				var divheight = 0;
				var divWidth = 0;
				var mainFancybox;
			var $= jQuery.noConflict();

						function doPopup(id){
							var renderOptions = {
											    force: true, // forces redrawing
											    animate: false, // redraws the widget without animation
											    asyncSeriesRendering: false,// redraws the widget synchronously
											}
							if(flag == 0)
							{
								flag = 1;
							 	$.fancybox({
							        href: '#'+id,
							        modal: false,
						          	padding    : 0,
    								margin: [20, 0, 20, 0],
    								closeEffect	: 'elastic',
							        width:750,
							        height:550,
							        autoCenter : false,
							        afterLoad  : function () {
							        	divheight = $('#'+id).height();
							        	divWidth =$('#'+id).width();
							            var ratio = 0.7;
    									$('#'+id).width($(window).width() * ratio).height($(window).height() * ratio);
    									//
    									if(id=='chartdiv')
								        {

								        	$('#'+id).toggleClass("pupupShadoeChartDiv");
								        }
								        else if(~id.indexOf("bar"))
										{
											$('#'+id).toggleClass("popupShadowBar");
										}
								        else if(~id.indexOf("chart"))
								        {

							        		$('#'+id).toggleClass("pupupShadowall");
										}
										else if(~id.indexOf("all"))
										{
											$('#'+id).toggleClass("pupupShadowall");

										}
							        },
						          	afterClose: function() {
								        $('#'+id).show();
								        $('#'+id).width(divWidth).height(divheight);

								        if(id=='chartdiv')
								        {
								        	//toastr.success('working');
								        	//alert('here');
											// $('#'+id).css('height', '250px');
											// $('#'+id).css('width', '455px');
											var chart = $('#'+id).dxPieChart('instance');
										 	chart.render(renderOptions);

										 	$('#'+id).toggleClass("pupupShadoeChartDiv");

								        }
								        else if(~id.indexOf("bar"))
										{
											$('#'+id).toggleClass('hidden');
											// toastr.success("yes");\
								        	$('#'+id).css('height', '230px');
											$('#'+id).css('width', '100%');
											var chart = $('#'+id).dxChart('instance');
										 	chart.render(renderOptions);
										 	$('#'+id).toggleClass("popupShadowBar");

										}
								        else if(~id.indexOf("chart"))
								        {
								        	$('#'+id).toggleClass('hidden');
								        	// toastr.success("yes");\
								   //      	$('#'+id).css('height', '230px');
											// $('#'+id).css('width', '100%');

											 // var chart = $('#'+id).dxPieChart('instance');
												//  chart.render(renderOptions);
											 $('#'+id).toggleClass("pupupShadowall");

											//alert("this");

										}
										else if(~id.indexOf("all"))
								        {
								        	// toastr.success("yes");\
								        	$('#'+id).css('height', '230px');
											$('#'+id).css('width', '100%');
											$('#'+id).toggleClass('hidden');
											 var chart = $('#'+id).dxPieChart('instance');
												 chart.render(renderOptions);
												 $('#'+id).toggleClass("pupupShadowall");

										}
								        flag= 0;

										//toastr.success(isMapFullscreened);

										isMapFullscreened = false;
										//toastr.success(isMapFullscreened);
								    }
						    	});

							  //  return false;
							}
							else
							{
								if(id=='chartdiv')
						        {
						        	//toastr.success('working');
									$('#'+id).css('height', '250px');
									$('#'+id).css('width', '455px');
									var chart = $('#'+id).dxPieChart('instance');
								 	chart.render(renderOptions);
								 	$('#'+id).toggleClass("pupupShadoeChartDiv");

						        }
						        else if(~id.indexOf("bar"))
								{
									// toastr.success("yes");\
						        	$('#'+id).css('height', '230px');
									$('#'+id).css('width', '100%');
									var chart = $('#'+id).dxChart('instance');
								 	chart.render(renderOptions);
								 	$('#'+id).toggleClass("popupShadowBar");

								}
						        else if(~id.indexOf("chart"))
						        {
						        	// toastr.success("yes");\
						        	$('#'+id).css('height', '230px');
									$('#'+id).css('width', '100%');

									 var chart = $('#'+id).dxPieChart('instance');
										 chart.render(renderOptions);
										 $('#'+id).toggleClass("pupupShadow");

								}
								else if(~id.indexOf("all"))
						        {
						        	// toastr.success("yes");\
						        	$('#'+id).css('height', '230px');
									$('#'+id).css('width', '100%');

									 var chart = $('#'+id).dxPieChart('instance');
										 chart.render(renderOptions);
										 $('#'+id).toggleClass("pupupShadowall");

								}

								$.fancybox.close();
								flag= 0;
								isMapFullscreened = false;
								//toastr.success(isMapFullscreened);
								toastr.success("this is working for map");

							}





						};
