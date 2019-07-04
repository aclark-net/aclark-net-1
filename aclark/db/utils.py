from django.db.models import F
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from .fields import get_fields
from .misc import has_profile
from .misc import set_items
from .page import paginate
from .query import get_query_string
from .search import get_search_results
from .total import get_total
from .total import set_total

gravatar_url = "https://www.gravatar.com/avatar/%s"


def get_index_items(**kwargs):
    """
    """
    context = {}
    model = kwargs.get("model")
    report_model = kwargs.get("report_model")
    filter_by = kwargs.get("filter_by")
    order_by = kwargs.get("order_by")
    page_size = kwargs.get("page_size")
    request = kwargs.get("request")
    search_fields = kwargs.get("search_fields")
    model_name = model._meta.verbose_name
    edit_url = "%s_edit" % model_name
    view_url = "%s_view" % model_name
    page_num = get_query_string(request, "page")
    paginated = get_query_string(request, "paginated")
    search = get_query_string(request, "search")

    items = {}
    if report_model:
        reports = report_model.objects.filter(active=True).order_by("-date")
        items = set_items("report", items=reports, _items=items)
    context["items"] = items
    context["%s_nav" % model_name] = True

    # Return search index items
    if request.method == "POST":
        if search == u"":  # Empty search returns none
            return context
        else:
            return get_search_results(
                context,
                model,
                search_fields,
                search,
                edit_url=edit_url,
                view_url=view_url,
                order_by=order_by,
                request=request,
            )
    # Return filtered or all index items
    if filter_by:
        items = model.objects.filter(**filter_by[model_name])
    else:
        items = model.objects.all()
    if order_by is not None:  # Order items
        # http://stackoverflow.com/a/20257999/185820
        items = items.order_by(*order_by)
    if not request.user.is_authenticated:  # Don't show items to anon
        items = []
    if paginated:  # Paginate if paginated
        page_size = get_setting(request, "page_size")
        items = paginate(items, page_num=page_num, page_size=page_size)
    context["edit_url"] = edit_url
    context["view_url"] = view_url
    context["page"] = page_num
    context["paginated"] = paginated
    items = set_items(model_name, items=items)
    context["items"] = items
    return context


def get_page_items(**kwargs):
    site_config_model = kwargs.get("site_config_model")
    contact_model = kwargs.get("contact_model")
    estimate_model = kwargs.get("estimate_model")
    invoice_model = kwargs.get("invoice_model")
    note_model = kwargs.get("note_model")
    model = kwargs.get("model")
    obj = kwargs.get("obj")
    project_model = kwargs.get("project_model")
    report_model = kwargs.get("report_model")
    request = kwargs.get("request")
    order_by = kwargs.get("order_by")
    pk = kwargs.get("pk")
    time_model = kwargs.get("time_model")
    filter_by = kwargs.get("filter_by")
    page_size = kwargs.get("page_size")
    context = {}
    items = {}
    time_include = ("date", "project", "hours", "log")
    user_include = ("rate", "bio", "dashboard_items")
    contact_include = ("first_name", "last_name")
    note_include = ("note",)

    if request:  # Applies to all page items
        doc = get_query_string(request, "doc")  # Export
        mail = get_query_string(request, "mail")  # Export
        pdf = get_query_string(request, "pdf")  # Export
        context["doc"] = doc
        context["mail"] = mail
        context["pdf"] = pdf
        context["request"] = request  # Include request

    model_name = None

    if model or obj:
        if model:
            model_name = model._meta.verbose_name
        elif obj:
            model_name = obj._meta.verbose_name

        context["model_name"] = model_name
        context["%s_nav" % model_name] = True
        context["edit_url"] = "%s_edit" % model_name
        context["view_url"] = "%s_view" % model_name

        if report_model:
            reports = report_model.objects.filter(active=True).order_by("-date")
            items = set_items("report", items=reports)

        context["items"] = items

        if model_name == "client":
            client = get_object_or_404(model, pk=pk)
            contacts = contact_model.objects.filter(client=client)
            estimates = estimate_model.objects.filter(client=client)
            invoices = invoice_model.objects.filter(client=client)
            projects = project_model.objects.filter(client=client)
            notes = note_model.objects.filter(client=client)
            if order_by:
                invoices = invoices.order_by(*order_by["invoice"])
                projects = projects.order_by(*order_by["project"])
            items = set_items("contact", items=contacts, _items=items)
            items = set_items("invoice", items=invoices, _items=items)
            items = set_items("note", items=notes, _items=items)
            items = set_items("project", items=projects, _items=items)
            items = set_items("estimate", items=estimates, _items=items)
            context["item"] = client
        elif model_name == "contact":
            contact = get_object_or_404(model, pk=pk)
            fields = get_fields(contact, include=contact_include)  # fields_items.html
            context["fields"] = fields
        elif model_name == "estimate":  # handle obj or model
            if not obj:
                estimate = get_object_or_404(model, pk=pk)
            else:
                estimate = obj
            times = time_model.objects.filter(estimate=estimate)
            if order_by:
                times = times.order_by(*order_by["time"])
            times = set_total(times, estimate=estimate)
            config = (
                site_config_model.get_solo()
            )  # get_solo will create the item if it does not already exist
            context["doc_type"] = model_name
            context["config"] = config
            context["entries"] = times
            context["item"] = estimate
        elif model_name == "invoice":
            invoice = get_object_or_404(model, pk=pk)
            config = (
                site_config_model.get_solo()
            )  # get_solo will create the item if it does not already exist
            times = time_model.objects.filter(estimate=None, invoice=invoice)
            times = times.order_by(*order_by["time"])
            times = set_total(times, invoice=invoice)
            last_payment_date = invoice.last_payment_date
            context["doc_type"] = model_name
            context["times"] = times
            context["item"] = invoice
            context["invoice"] = True
            context["config"] = config
            context["last_payment_date"] = last_payment_date
        elif model_name == "project":
            project = get_object_or_404(model, pk=pk)
            contacts = contact_model.objects.all()
            estimates = estimate_model.objects.filter(project=project)
            invoices = invoice_model.objects.filter(project=project)
            notes = note_model.objects.filter(project=project)
            times = time_model.objects.filter(
                estimate=None, project=project, task__isnull=False, invoiced=False
            )
            times = set_total(times, project=project, time_model=time_model)
            if order_by:
                times = times.order_by(*order_by["time"])
                invoices = invoices.order_by(*order_by["invoice"])
            items = set_items("contact", items=contacts, _items=items)
            items = set_items("estimate", items=estimates, _items=items)
            items = set_items("invoice", items=invoices, _items=items)
            items = set_items("time", items=times, _items=items)
            items = set_items("note", items=notes, _items=items)
            context["item"] = project
            context["cost"] = float(project.cost)
            context["gross"] = float(project.amount)
            context["net"] = float(project.amount) - float(project.cost)
        elif model_name == "report":
            report = get_object_or_404(model, pk=pk)
            reports = model.objects.filter(active=True).order_by("-date")
            reports.aggregate(cost=Sum(F("cost")))
            reports.aggregate(gross=Sum(F("gross")))
            reports.aggregate(net=Sum(F("net")))
            invoices = report.invoices.all()
            items = set_items("invoice", items=invoices, _items=items)
            items = set_items("report", items=reports, _items=items)
            context["item"] = report
            # E-Mail
            context["message"] = "Cost: %s, Gross: %s, Net: %s" % (
                report.cost,
                report.gross,
                report.net,
            )
            context["subject"] = report.name
        elif model_name == "task":
            task = get_object_or_404(model, pk=pk)
            context["item"] = task
        if model_name == "time":
            time = get_object_or_404(model, pk=pk)
            context["item"] = time
            fields = get_fields(time, include=time_include)  # fields_table.html
            context["fields"] = fields  # fields_items.html
        elif model_name == "user":
            user = get_object_or_404(model, pk=pk)
            projects = project_model.objects.filter(team__in=[user], active=True)
            projects = projects.order_by(*order_by["project"])
            times = time_model.objects.filter(estimate=None, invoiced=False, user=user)
            times = times.order_by(*order_by["time"])
            contacts = contact_model.objects.all()
            fields = get_fields(user.profile, include=user_include)  # fields_table.html
            hours = get_total("hours", times=times)
            context["fields"] = fields
            context["item"] = user
            context["projects"] = projects
            context["times"] = times
            context["hours"] = hours
        elif model_name == "note":
            note = get_object_or_404(model, pk=pk)
            fields = get_fields(note, include=note_include)  # fields_items.html
            context["fields"] = fields
            context["item"] = note
        else:
            item = get_object_or_404(model, pk=pk)
            context["item"] = item
    else:  # no model or obj
        if request:
            if request.user.is_authenticated:
                # Items
                invoices = invoice_model.objects.filter(last_payment_date=None)
                invoices = invoices.order_by(*order_by["invoice"])
                projects = project_model.objects.filter(active=True, hidden=False)
                projects = projects.order_by(*order_by["project"])
                if filter_by:
                    times = time_model.objects.filter(**filter_by["time"])
                else:
                    times = time_model.objects.all()
                times = times.order_by(*order_by["time"])
                times = set_total(times)
                items = set_items("invoice", items=invoices)
                items = set_items("project", items=projects, _items=items)
                items = set_items("time", items=times, _items=items)
                # Paginate items
                page_num = get_query_string(request, "page")
                paginated = get_query_string(request, "paginated")
                if paginated:  # Paginate if paginated
                    page_size = get_setting(request, "page_size")
                    if "times" in items:
                        items["times"] = paginate(
                            items["times"], page_num=page_num, page_size=page_size
                        )
                # Totals
                net = 0
                gross = get_total("gross", invoices=invoices)
                hours = get_total("hours", times=times)
                cost = get_total("cost", projects=projects)
                if gross and cost:
                    net = gross - cost
                context["net"] = net
                context["gross"] = gross
                context["hours"] = hours
                context["cost"] = cost

                # Location
                ip_address = request.META.get("HTTP_X_REAL_IP")
                context["ip_address"] = ip_address

                # Reports
                reports = report_model.objects.filter(active=True).order_by("-date")
                items = set_items("report", items=reports, _items=items)
                context["items"] = items
    return context


def get_setting(request, setting, settings_model=None, page_size=None):
    """
    Return appropriate setting from user profile model or singleton settings
    model based on args
    """
    if not request.user.is_authenticated:
        return
    if setting == "icon_size":
        if has_profile(request.user):
            user_pref = request.user.profile.icon_size
        if user_pref:
            return user_pref
    elif setting == "icon_color":
        if has_profile(request.user):
            user_pref = request.user.profile.icon_color
        if user_pref:
            return user_pref
    elif setting == "page_size":
        if has_profile(request.user):
            user_pref = request.user.profile.page_size
        if user_pref:
            return user_pref
    elif setting == "dashboard_choices":
        if has_profile(request.user):
            user_pref = request.user.profile.dashboard_choices
        if user_pref:
            return user_pref


def set_ref(obj, request, **kwargs):
    """
    Set object field references after create or edit
    """
    client_model = kwargs.get("client_model")
    estimate_model = kwargs.get("estimate_model")
    invoice_model = kwargs.get("invoice_model")
    project_model = kwargs.get("project_model")
    model_name = obj._meta.verbose_name
    if model_name == "contact":
        query_client = get_query_string(request, "client")
        if query_client:
            client = get_object_or_404(client_model, pk=query_client)
            obj.client = client
            obj.save()
    elif model_name == "estimate" or model_name == "invoice":
        query_client = get_query_string(request, "client")
        query_project = get_query_string(request, "project")
        if query_project:
            project = get_object_or_404(project_model, pk=query_project)
            obj.client = project.client
            obj.project = project
            obj.save()
        if query_client:
            client = get_object_or_404(client_model, pk=query_client)
            obj.client = client
            obj.save()
    elif model_name == "note":
        query_client = get_query_string(request, "client")
        query_invoice = get_query_string(request, "invoice")
        if query_client:
            client = get_object_or_404(client_model, pk=query_client)
            client.note.add(obj)
            client.save()
        elif query_invoice:
            invoice = get_object_or_404(invoice_model, pk=query_invoice)
            invoice.note.add(obj)
            invoice.save()
    elif model_name == "project":
        query_client = get_query_string(request, "client")
        if query_client:
            client = get_object_or_404(client_model, pk=query_client)
            obj.client = client
            obj.save()
    elif model_name == "time":
        if not obj.user:  # If no user, set user, else do nothing.
            obj.user = request.user
        query_estimate = get_query_string(request, "estimate")
        query_invoice = get_query_string(request, "invoice")
        query_project = get_query_string(request, "project")
        if query_estimate:
            estimate = get_object_or_404(estimate_model, pk=query_estimate)
            obj.estimate = estimate
        if query_invoice:
            invoice = get_object_or_404(invoice_model, pk=query_invoice)
            obj.invoice = invoice
            obj.save()  # Need save here to set more attrs
            obj.project = invoice.project
            obj.save()  # Need save here to set more attrs
            obj.task = invoice.project.task
        if query_project:
            project = get_object_or_404(project_model, pk=query_project)
            obj.project = project
            obj.save()  # Need save here to set more attrs
            if project.task:
                obj.task = project.task
        obj.save()
