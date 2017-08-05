# JMI
**_JNI Modern Interface in C++_**

### Features

- Support both In & Out parameters for JNI methods
- Per class jclass cache, per method jmethodID cache, per field jfieldID cache
- The same C++/Java linkage: a static java member maps to a static member in C++
- getEnv() at any thread without caring about when to detach
- Signature is generated by compiler only once
- Easy to use

### Example:
- Setup java vm in `JNI_OnLoad`: `jmi::javaVM(vm);`

- Create a SurfaceTexture: 
```
    // define SurfaceTexture tag class in any scope visibile by jmi::JObject<SurfaceTexture>
    struct SurfaceTexture : jmi::ClassTag { static std::string name() {return "android/graphics/SurfaceTexture";}};
    ...
    GLuint tex = ...
    ...
    jmi::JObject<SurfaceTexture> texture;
    if (!texture.create(tex)) {
        // texture.error() ...
    }
```

- Create Surface from SurfaceTexture:
```
    struct Surface : jmi::ClassTag { static std::string name() {return "android.view.Surface";}}; // '.' or '/'
    ...
    jmi::JObject<Surface> surface;
    surface.create(texture);
```

- Call void method:
```
    texture.call("updateTexImage");
```

- Call method with output parameters:
```
    float mat4[16]; // or std::array<float, 16>, valarray<float>
    texture.call("getTransformMatrix", std::ref(mat4)); // use std::ref() if parameter should be modified by jni method
```

- Call method with a return type:
```
    jlong t = texture.call<jlong>("getTimestamp");
```

## jmethodID Cache

`call("methodName", ....)`/`callStatic("methodName", ....)` always invokes `GetMethodID()`/`GetStaticMethodID()`. To avoid this and invoke only once for each method of a java class, use overload one `call<...MTag>(...)`, where `MTag` is a subclass of `jmi:MethodTag` implementing `static const char* name() { return "methodName";}`.

```
    // GetMethodID() will be invoked only once for each method in the scope of MethodTag subclass
    struct UpdateTexImage : jmi::MethodTag { static const char* name() {return "updateTexImage";}};
    struct GetTimestamp : jmi::MethodTag { static const char* name() {return "getTimestamp";}};
    struct GetTransformMatrix : jmi::MethodTag { static const char* name() {return "getTransformMatrix";}};
    ...
    texture.call<UpdateTexImage>();
    jlong t = texture.call<jlong, GetTimestamp>();
    texture.call<GetTransformMatrix>(std::ref(mat4)); // use std::ref() if parameter should be modified by jni method
```

### Field API

Field api supports cacheable and uncacheable jfieldID

Cacheable jfieldID through FieldTag

```
    JObject<MyClass> obj;
    ...
    struct MyIntField : FieldTag { static const char* name() {return "myIntFieldName";} };
    auto ifield = obj.field<int, MyIntField>();
    jfieldID ifid = ifield; // or ifield.id()
    ifield.set(1234);
    int ivalue = ifield; // or ifield.get();

    // static field is the same except using the static function JObject::staticField
    struct MyStrFieldS : FieldTag { static const char* name() {return "myStaticStrFieldName";} };
    auto& ifields = JObject<MyClass>::staticField<std::string, MyIntFieldS>(); // it can be an ref
    jfieldID ifids = ifields; // or ifield.id()
    ifields.set("JMI static field test");
    std::string ivalues = ifields; // or ifield.get();
```

Uncacheable jfieldID using field name string directly

```
    auto ifield = obj.field<int>("myIntFieldName");
    ...
```


### Known Issues

- If return type and first n arguments of call/call_static are the same, explicitly specifying return type and n arguments type is required

### Why JObject is a Template?
- To support per class jclass, per method jmethodID, per field jfieldID cache

#### Tested Platforms

macOS clang & g++7, android clang & g++-4.9

#### MIT License
>Copyright (c) 2016-2017 WangBin

