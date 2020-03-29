from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Tags,Labels,Zeros,ToParse,BoostModels
from .serializers import TagsSerializer,LabelsSerializer,ZerosSerializer

# from threading import Thread
# from django.db import connection

import ToParsee

class tagsView(APIView):
    def get(self, request):
        tags = Tags.objects.all()
        serializer = TagsSerializer(tags, many=True)
        return Response({"tags": serializer.data})

    def post(self, request):
        rq = request.data.get('request')
        serializer = TagsSerializer(data=rq)

        if serializer.is_valid(raise_exception=True):
            tag_saved = serializer.save()
        return Response({"success": "Article '{}' created successfully".format(tag_saved.label)})

class labelsView(APIView):
    def get(self, request):
        labels = Labels.objects.all()
        serializer = LabelsSerializer(labels, many=True)
        return Response({"labels": serializer.data})

    def post(self, request):
        rq = request.data.get('request')
        serializer = LabelsSerializer(data=rq)
        if serializer.is_valid(raise_exception=True):
            label_saved = serializer.save()
        return Response({"success": "Article '{}' created successfully".format(label_saved.name)})

class zerosView(APIView):
    def get(self, request):
        zeros = Zeros.objects.all()
        serializer = ZerosSerializer(zeros, many=True)
        return Response({"zeros": serializer.data})

    def post(self, request):
        rq = request.data.get('request')
        serializer = ZerosSerializer(data=rq)
        if serializer.is_valid(raise_exception=True):
            zero_saved = serializer.save()
            # tags = Tags.objects.all()
            # zeros = Zeros.objects.all()
            # trainDataset = [tags.filter(label=zero_saved.true_label).values_list('label','data'),zeros.filter(true_label = zero_saved.true_label).values_list('true_label','data')]
            # model = ToParsee.PtrainM(trainDataset)
            # BoostModels(Bmodel = model,label=zero_saved.true_label).save()
        return Response({"success": "Article '{}' created successfully".format(zero_saved.true_label)})



# def sync_get_urls(query,count):
#     return sync_to_async(ToParsee.url_find(query,count))()

# def sync_get_datas():
#     return sync_to_async(ToParse.objects.all())()

# def sync_get_sites():
#     return sync_to_async(ToParse.objects.all().values('site'))()

# async def urlWrapper(query,count):
#     return await sync_get_urls(query,count)
# async def datasWrapper():
#     return await sync_get_datas()
# async def sitesWrapper():
#     return await sync_get_sites()
# def start_new_thread(function):
#     def decorator(*args, **kwargs):
#         t = Thread(target = function, args=args, kwargs=kwargs)
#         t.daemon = True
#         t.start()
#     return decorator    


# @start_new_thread
# def site_links(query,count):
#     a = ToParsee.url_find(query,count)
#     connection.close()
#     return a

# @start_new_thread
# def datas():
#     a = ToParse.objects.all()
#     connection.close()
#     return a

# @start_new_thread
# def sites():
#     a = ToParse.objects.all().values('site')
#     connection.close()
#     return a
class Parse(APIView):
    def get(self, request):
        # ToParsee.PtrainM([],[])
        query = str(request.GET['query'])
        count = int(request.GET['count'])
        print(query,count)
        # labels_count = len(Labels.objects.all())
        # datas = ToParse.objects.all()
        # sites = datas.values('site')
        labels = []
        for i in Tags.objects.filter(used=True).values('label').distinct():
            # print(Tags.objects.filter(used = True,label=i['label']))
            if len(Tags.objects.filter(used = True,label=i['label']))%10 == 0:
                labels.append(i['label'])
        if labels != []:
            models = BoostModels.objects.filter(label__in=labels)
            # Mlabels = models.values('label')
            site_links = ToParsee.url_find(query,count)#urlWrapper(query,count)
            # counter = False#True #счетки кол-ва добавленных тегов нужного лейбла
            for i in site_links:
                print(i)
                url_ = ''
                try:
                    url_ = i.split('https://')[1]
                except:
                    url_ = i.split('http://')[1]
                url_ = url_.split('/')[0]
                if url_.split('.')[0] == 'www':
                    url_ = ''.join(url_.split('.')[1:-1])
                else:
                    url_ = ''.join(url_.split('.')[0:-1])
                # Tags.objects.all().filter(label=label,used=True)
                ToParse.objects.filter(site=url_).delete()

                f = ToParsee.AgenerateP(i,models.values_list('Bmodel'),url_)[0]
                # print(f)
                # if f:
                for j in f:
                    # print(j)
                    obj = ToParse(site=j['site'],tag=j['tag'],Cclass=j['class'],ptag=j['ptag'],pptag=j['pptag'],pclass=j['pclass'],ppclass=j['ppclass'])
                    obj.save()
        datas = list(ToParse.objects.all().values())#datasWrapper()
        sites = list(ToParse.objects.all().values('site'))#sitesWrapper()
        # print(datas)
        res = ToParsee.asyncParse(site_links = site_links,sites = sites,datas = datas)
        return Response({"data": res})

        # res = defs.get_query(sites = sites,datas = datas,query=query,count=count)


class Trainer(APIView):
    def post(self,request):
        data = request.data.get('request')
        label,params = data['label'],data['params']
        # counter = len(Tags.objects.filter(label=label))
        tags = Tags.objects.all().filter(label=label,used=False)
        if len(tags) % 10 == 0:
            zeros = Zeros.objects.all().filter(true_label = label,used=False)
            trainDataset = [tags.values_list('data'),zeros.values_list('data')]
            if trainDataset[0] and trainDataset[1]:
                prevmodel = BoostModels.objects.filter(label=label)
                # tags,zeros = tags.get(),zeros.get()
                tags.update(used = True)
                zeros.update(used = True)
                # model = BoostModels.objects.filter(label=label).exists()
                if prevmodel.exists():
                    # print(prevmodel.values_list('Bmodel'))
                    model = ToParsee.APtrainM(trainDataset,params,prev_model = prevmodel.values_list('Bmodel')[0][0])
                    # prevmodel = prevmodel.get()
                    # prevmodel.Bmodel = model
                    # prevmodel.save()
                    prevmodel.update(Bmodel = model)
                else:
                    model = ToParsee.APtrainM(trainDataset,params)
                    BoostModels(Bmodel = model,label=label).save()
        return Response({"success": "Trainer"})
# def trainAndAdd():








        # res = defs.asyncParse(site_links = site_links,sites = sites,datas = datas)

        # res = defs.get_query(sites = sites,datas = datas,query=query,count=count)
        # zeros = Zeros.objects.all()
        # serializer = ZerosSerializer(zeros, many=True)
        # return Response({"zeros": serializer.data})