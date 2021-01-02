--
-- File generated with SQLiteStudio v3.2.1 on Fri Jan 1 18:13:50 2021
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: available_time
DROP TABLE IF EXISTS available_time;

CREATE TABLE available_time (
    StaffID  VARCHAR (10) NOT NULL
                          CHECK ("StaffID" LIKE 'G%'),
    Timeslot DATETIME     NOT NULL,
    FOREIGN KEY (
        StaffID
    )
    REFERENCES Users (ID) ON DELETE CASCADE
                          ON UPDATE CASCADE
);

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G01',
                               '2020-12-25 11:00:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G01',
                               '2020-12-25 9:00:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G01',
                               '2020-12-25 9:15:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G01',
                               '2020-12-25 9:30:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G01',
                               '2020-12-30 9:00:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G01',
                               '2020-12-30 9:15:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G01',
                               '2020-12-30 9:30:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G02',
                               '2020-12-25 14:00:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G03',
                               '2020-12-25 14:00:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G03',
                               '2020-12-30 9:00:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G01',
                               '2021-01-03 09:00:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G01',
                               '2021-01-03 09:15:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G01',
                               '2021-01-03 09:30:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G01',
                               '2021-01-03 09:45:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G01',
                               '2021-01-03 10:00:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G01',
                               '2021-01-03 13:15:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G01',
                               '2021-01-03 10:30:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G01',
                               '2021-01-03 13:00:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G01',
                               '2021-01-05 11:15:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G01',
                               '2021-01-03 11:30:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G02',
                               '2021-01-02 17:45:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G03',
                               '2021-01-02 12:00:00'
                           );

INSERT INTO available_time (
                               StaffID,
                               Timeslot
                           )
                           VALUES (
                               'G01',
                               '2021-01-02 12:15:00'
                           );


-- Table: GP
DROP TABLE IF EXISTS GP;

CREATE TABLE GP (
    ID             VARCHAR (10) CHECK ("ID" LIKE 'G%'),
    Gender         CHAR (1)     CHECK (Gender IN ('M', 'F', 'N') ),
    ClinicAddress  BLOB,
    ClinicPostcode BLOB,
    Speciality     BLOB,
    Introduction   BLOB,
    Rating         INT          DEFAULT 0
                                CHECK ("Rating" >= 0 OR 
                                       "Rating" <= 5),
    PRIMARY KEY (
        ID
    ),
    FOREIGN KEY (
        ID
    )
    REFERENCES Users (ID) ON DELETE CASCADE
                          ON UPDATE CASCADE
);

INSERT INTO GP (
                   ID,
                   Gender,
                   ClinicAddress,
                   ClinicPostcode,
                   Speciality,
                   Introduction,
                   Rating
               )
               VALUES (
                   'G01',
                   'F',
                   X'6741414141414266364F6C6746434C37626D737A69797555662D6447305A384764766A5F5A47456E6D703763315868424D58776D5A3152414565374F34544D4B7359342D363066497730326D686F324A533276795F73426E33564455366D494F4776584A46776A766B7271486D4B7A434C5378766E7A6B3D',
                   X'6741414141414266364F6C675F6F685A5F6151757057644D7A652D7734797944695476796F69504B6C636B486243626B6E35574C75754D562D32316E643243744D66795575397069706E6D30657646786B585A30654F64685F3279306C6C636979673D3D',
                   'Pediatrics',
                   'Hi,I am G01. I am good at getting along with the children',
                   5
               );

INSERT INTO GP (
                   ID,
                   Gender,
                   ClinicAddress,
                   ClinicPostcode,
                   Speciality,
                   Introduction,
                   Rating
               )
               VALUES (
                   'G02',
                   'M',
                   X'6741414141414266364F6C67427576494C73687669534F2D4F65504F576C33767962396342354155727A5F556C6659635849426F4F5970474E4C76435049653877513166764C75556E4F7A5074627638367A6A3671595F3361464B544A7672707A57366A465F51427764333333654271764F306D4F6A493D',
                   X'6741414141414266364F6C67764762794F383967754C496734525A5F674F507572706F6E436E574F764D32676D534F3374794866665A4869516873534B30666F35746B576B6E376474326A4D6F7637334279724D374D455841562D342D61323038673D3D',
                   'Orthopedics',
                   'Hi,I am G02. Strong and gentle.',
                   4
               );

INSERT INTO GP (
                   ID,
                   Gender,
                   ClinicAddress,
                   ClinicPostcode,
                   Speciality,
                   Introduction,
                   Rating
               )
               VALUES (
                   'G03',
                   'M',
                   X'6741414141414266364F6C674762635F455463734F424B4B745245614777306A346F726673516670367432594A396378337355464A796A755833512D7835555F71446363515477414257506673324B694F7544377A3241397134785355763153554A706E337971543170474250645F346C7466446C684D3D',
                   X'6741414141414266364F6C6745516F5372784B4B4B436D6353565F6F69503966746B6F4C505657537835335244714E375A65504446456B6A587776635569494E2D6566424933585755306A7335686C6863346A544F35755A675841704B47304D35513D3D',
                   'Cardiology',
                   'Hi,I am G03. Take me to your heart',
                   4
               );


-- Table: Patient
DROP TABLE IF EXISTS Patient;

CREATE TABLE Patient (
    NHSNo        VARCHAR (10) CHECK ("NHSNo" BETWEEN 1000000000 AND 9999999999),
    Gender       CHAR (1)     CHECK (Gender IN ('M', 'F', 'N') ),
    Introduction BLOB,
    Notice       BLOB,
    PRIMARY KEY (
        NHSNo
    ),
    FOREIGN KEY (
        NHSNo
    )
    REFERENCES Users (ID) ON DELETE CASCADE
                          ON UPDATE CASCADE
);

INSERT INTO Patient (
                        NHSNo,
                        Gender,
                        Introduction,
                        Notice
                    )
                    VALUES (
                        '1929282829',
                        'F',
                        'I am an accountant',
                        'penicillin allergy'
                    );

INSERT INTO Patient (
                        NHSNo,
                        Gender,
                        Introduction,
                        Notice
                    )
                    VALUES (
                        '2929282822',
                        'M',
                        'I am a basketball player',
                        'gluten intolerance'
                    );

INSERT INTO Patient (
                        NHSNo,
                        Gender,
                        Introduction,
                        Notice
                    )
                    VALUES (
                        '3334567878',
                        'M',
                        'I am a sales manager',
                        'diabetes'
                    );


-- Table: prescription
DROP TABLE IF EXISTS prescription;

CREATE TABLE prescription (
    PrescriptionNumber INTEGER,
    BookingNo          INT     NOT NULL,
    drugName           BLOB    NOT NULL,
    quantity           BLOB    NOT NULL,
    Instructions       BLOB    NOT NULL,
    PRIMARY KEY (
        PrescriptionNumber
    ),
    FOREIGN KEY (
        BookingNo
    )
    REFERENCES VisitBooking (BookingNo) ON DELETE CASCADE
                                        ON UPDATE CASCADE
);

INSERT INTO prescription (
                             PrescriptionNumber,
                             BookingNo,
                             drugName,
                             quantity,
                             Instructions
                         )
                         VALUES (
                             1,
                             1,
                             'Vitamin C',
                             '60 pills',
                             'take 1 or 2 pills after meals '
                         );

INSERT INTO prescription (
                             PrescriptionNumber,
                             BookingNo,
                             drugName,
                             quantity,
                             Instructions
                         )
                         VALUES (
                             2,
                             2,
                             'Aspirin',
                             '6 capsules * 3',
                             'take 0ne capsule after breakfast and dinner'
                         );

INSERT INTO prescription (
                             PrescriptionNumber,
                             BookingNo,
                             drugName,
                             quantity,
                             Instructions
                         )
                         VALUES (
                             3,
                             3,
                             'IV ',
                             '500ml *2bottles* 3days',
                             'following 3 days in hospital'
                         );

INSERT INTO prescription (
                             PrescriptionNumber,
                             BookingNo,
                             drugName,
                             quantity,
                             Instructions
                         )
                         VALUES (
                             4,
                             584540,
                             X'6741414141414266376A333532526B6E6F66396A4B464D4861684237413658325872674531716A7556334657513631556767395773766A506A4C543242564167675868563867397A4969424E465F41563076454E4B4F6B4175553034304F34574F673D3D',
                             X'6741414141414266376A333568495F363365515A446E665073576E694F6166617A767445562D6F4E37435F4368755237746849504F6F50367569686A484B315365553752354467714E6D79423676647A437A6E6F726245554E33464B6E64454531513D3D',
                             X'6741414141414266376A333557476B774D6658326C4E5545623067484A3857485265673071594531354C4F675952596634764E7943765456575137495F397243374E303748716352566565416D5544585A75484D413633534443536331576D7565513D3D'
                         );


-- Table: UserGroup
DROP TABLE IF EXISTS UserGroup;

CREATE TABLE UserGroup (
    UserType VARCHAR (10) PRIMARY KEY
);

INSERT INTO UserGroup (
                          UserType
                      )
                      VALUES (
                          'GP'
                      );

INSERT INTO UserGroup (
                          UserType
                      )
                      VALUES (
                          'Admin'
                      );

INSERT INTO UserGroup (
                          UserType
                      )
                      VALUES (
                          'Patient'
                      );


-- Table: Users
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    ID          VARCHAR (10) CHECK ( ("ID" LIKE 'G%') OR 
                                     ("ID" LIKE 'A%') OR 
                                     ("ID" BETWEEN 1000000000 AND 9999999999) ),
    username    VARCHAR (50) NOT NULL
                             UNIQUE,
    passCode    VARCHAR (64) NOT NULL,
    birthday    BLOB,
    firstName   BLOB,
    lastName    BLOB,
    phoneNo     BLOB,
    HomeAddress BLOB,
    postCode    BLOB,
    UserType    VARCHAR (10) NOT NULL,
    Deactivated CHAR (1)     DEFAULT 'T'
                             CHECK (Deactivated IN ('T', 'F') ),
    LoginCount  INTEGER      NOT NULL
                             DEFAULT 0,
    PRIMARY KEY (
        ID
    ),
    FOREIGN KEY (
        UserType
    )
    REFERENCES UserGroup (UserType) ON DELETE CASCADE
                                    ON UPDATE CASCADE
);

INSERT INTO Users (
                      ID,
                      username,
                      passCode,
                      birthday,
                      firstName,
                      lastName,
                      phoneNo,
                      HomeAddress,
                      postCode,
                      UserType,
                      Deactivated,
                      LoginCount
                  )
                  VALUES (
                      'G01',
                      'testGP',
                      '061962bb8a2c6dec570289487cf441f685c083062bc73941f9a679e9761b0925',
                      X'6741414141414266364F6C6777426C7376797A664938753775573159374435387848546D4F6F735341335F5A495751735474737636616E617538427A3553304D316F6A773059655174486139704C566456394F616F4C6549467A64306B4C596A4A513D3D',
                      X'6741414141414266364F6C67685762377939524559654E706F4A5034775A665932466876686F4768554B69574E392D526641414C4A627972477A4D75454C6B3145382D315336534368466F41782D384D333546524A68767635442D754E56636E43773D3D',
                      X'6741414141414266364F6C676A4C6551565143385664786D72723530414133342D754F764750626D7A345A2D77544B62764570746C5168473856384A4D5673525A55554B70516C5F4C4879642D714245664E7751375A49743359716E5953384567413D3D',
                      X'6741414141414266364F6C67697A67464F6341357854725A41305A707A346C326F696B5354394969766C676F564B576776425F6D7150583348705772685866534F75515567726977643743594936796D5F4C33776C6C58744C6A6D452D6867396F773D3D',
                      X'6741414141414266364F6C6770677462656B354F6A633554713949694C6E69356B66346742575957522D6F2D3978463556647737516E772D572D61734D315249747646474C5A576F673542507236424D614C687042647037736B37452D746B714C75624E584254754A7A4E784A566843416455585471343D',
                      X'6741414141414266364F6C6732387038706D49745951387770527475555949396B593541316B694A4679384A6E775771304A6742716963497058626A59746332386A4745524F727335304C575F3868375867744C546B4D4B6531317A5374393249413D3D',
                      'GP',
                      'F',
                      0
                  );

INSERT INTO Users (
                      ID,
                      username,
                      passCode,
                      birthday,
                      firstName,
                      lastName,
                      phoneNo,
                      HomeAddress,
                      postCode,
                      UserType,
                      Deactivated,
                      LoginCount
                  )
                  VALUES (
                      'G02',
                      'testGP2',
                      '23730ea22929f446a38020deecace3c4194346d102f0a2c380beac15916a29d8',
                      X'6741414141414266364F6C676369494B685654485A54595A51506A744B5144767849727567325F5454536C5A62344C6C5468636C4D654843373644626A47326638726F4850666B6937303367496476556252415551336E32526654495A672D6253673D3D',
                      X'6741414141414266364F6C677A50323276585A6C4B6862754C4D466F4A763377634C2D794D496A63764351726271435F50772D64544E4B47545F534C6F39773975384A6366327A476D6249437765746C315748785F664C7131487A444A3536696B5F6D4E415A364E7961743935485356735478456B786B3D',
                      X'6741414141414266364F6C674E6E397766305A4346654C5158747A4761346B696646675644643047795131314B683135537A68426444685145634161496E76664570366C6635453877486A544335315A5442362D5874624A4D576776512D7368694F71524C777369346E3942354E76446674435A3674673D',
                      X'6741414141414266364F6C67386F6D7355347178635946374D5A7544676238686B3235616C583150584F536645474776616879744B646A71744552667A7A4257666963446349536F74727947336F7066317847446B5A714B49454C7A694F777A2D413D3D',
                      X'6741414141414266364F6C67386A466F796B394D704F48577A695A5A6D7A624B4C594C6652486E71356A4C4738376F5665454939346C684D624F324139523452424277482D58576B664E61796536635163496271507133643159725A6B773369726D5A7769447946463379654666487836634F6E516D733D',
                      X'6741414141414266364F6C676A74345F3759564F4F736E4B495A736A36764332777036507A705F434D366C6B676659514F455A647654485948634E5F565163526E39326D785F574D6254585956365266356136796A3756315444696A5F38374A31773D3D',
                      'GP',
                      'F',
                      0
                  );

INSERT INTO Users (
                      ID,
                      username,
                      passCode,
                      birthday,
                      firstName,
                      lastName,
                      phoneNo,
                      HomeAddress,
                      postCode,
                      UserType,
                      Deactivated,
                      LoginCount
                  )
                  VALUES (
                      'G03',
                      'testGP3',
                      'ebe1e6b8490f120ab3c0bb8f8adab18fede550926089a8c5ac2d52617d0cc834',
                      X'6741414141414266364F6C67334E68304B484B7345636C635051532D5732486F49705F4430676B777367663470706A334E3750325F583632745A58464F75474C6F35736D4D754E71616F7852766B78446C575852734B7236384C4949612D716279513D3D',
                      X'6741414141414266364F6C674847415A576B2D3157492D784B5A50756F4237524F324945774A6348394F5857717935724F52495379465179566C745A47696631345A475F4B4567506F434271706F516B535744507373704B6F6D346E77517A67376C465838374B49556D5A5262374C69445857594D6D553D',
                      X'6741414141414266364F6C6743756F385156375776364B744F456C525A4D70546531556C4869526136747162647069486E55715944394C39306F6334694D3749416B4D41686458505265737A51365146505A4E663174397641565F31483143305A71774261527A4B504D637854514C56716878774E644D3D',
                      X'6741414141414266364F6C6742596F73485F4B3137596D55335676585A754E77676E6D4A68487066782D3066675745583554334553506144574D2D6F4A6D6559704B4277434E727A6F564D6764774D7A36497853536D5F374D3034753570616E70413D3D',
                      X'6741414141414266364F6C67502D4141346C644434326F68743238443551364F33664342503844533754456950445633526B3861324244654E52713455796557346F51575273314151545F4866553057734F70646F614B54394677374C3073516D574F7A7036744B4650614D30757035445F7844364F493D',
                      X'6741414141414266364F6C674E3374765353486B36435952627344526430466D5A65524D646154375562502D56533944514357364D654C425546596C4755334B4735355635684E71564543394E697555462D4F553556796F58584A777566585F36513D3D',
                      'GP',
                      'F',
                      0
                  );

INSERT INTO Users (
                      ID,
                      username,
                      passCode,
                      birthday,
                      firstName,
                      lastName,
                      phoneNo,
                      HomeAddress,
                      postCode,
                      UserType,
                      Deactivated,
                      LoginCount
                  )
                  VALUES (
                      '1929282829',
                      't',
                      '5c62e091b8c0565f1bafad0dad5934276143ae2ccef7a5381e8ada5b1a8d26d2',
                      X'6741414141414266364F6C676A4A5A6765314D4B314F6755466B6B6D5838714A4149416E4B6F523231425747785531303638417937446E7472424D4A6A507043526942395F4C4C31364C5F4E424853654254654B464750654D59675A4B33725832413D3D',
                      X'6741414141414266364F6C67626579576371734275324E55584F6B4C3830614C6F34316238744F5152377671574D614274654E7549777A7A565648313164793973486E67325677486E7232696F6D6B583170386B62543270477951714250584365324771456A32304D386572707931746C3065644B34513D',
                      X'6741414141414266364F6C6735713176464572586F4C49774573757A7452316F777049445A685043736B4E395F5757414D43476C6848655976744470373476453949797756344C684D4D4C2D386D5361397439485A65774B34746A62556B4C53424E314152584E58776B565235506A6C4B7054447664633D',
                      X'6741414141414266364F6C67364263786E6D3542653462593461356E6648703152584D564F596A646F683838756278784649446849702D794E476D71765735796C49386474354B32537738416A343842584357745F3154706D786C6B45476B7956773D3D',
                      X'6741414141414266364F6C67464458335872574C735573714D334A2D366B5863554434503350774477775F654335775A756F39484248324B7067377476385055774F764D6D7A68565457626947616F46706D57615F465058662D6F6D476B72664C685A44475442484E6153634E6B3952784C715279796B744E71414C4B6C396532723544594A535970705875',
                      X'6741414141414266364F6C67336269714C4C7A5872426D6B364E5339484773394262396A516F4B6F324E51324574516264364D5876356A337362764E4D354E515236716C616C515976336F79726972336E566D30304370634F654C724E4D415661413D3D',
                      'Patient',
                      'F',
                      0
                  );

INSERT INTO Users (
                      ID,
                      username,
                      passCode,
                      birthday,
                      firstName,
                      lastName,
                      phoneNo,
                      HomeAddress,
                      postCode,
                      UserType,
                      Deactivated,
                      LoginCount
                  )
                  VALUES (
                      '2929282822',
                      'testPatient2',
                      '99eaac23c002c5cda7e27a305d34d865d3d12541888ee42bdce7e50ca7fc2c35',
                      X'6741414141414266364F6C676B70357431575546697867487849316A734E456F5461665A796A764C667A7835716754644A50516271486C3476355245372D435F77543662444C675148447A614C634845394B45684C4D2D77424A37375652433848513D3D',
                      X'6741414141414266364F6C67436D346479623153757A734773756F43794C62613634793152436D4B4E584E5F744A41346949516947563155666936715071717865795A68456852675854326F762D67786C6D425361586745654737777364525A6872335252746E354F764E4546777543546A6B45506C6B3D',
                      X'6741414141414266364F6C6746354A55734C5F72785449626E577457547A585F3674313031566E7251387A5F5663475A5834733536725169597870544F356C344C6266446C66534432725A4B69487064455635596E41547879336D486E56337148654531462D4C6A6C58493859576C434D5039703176673D',
                      X'6741414141414266364F6C676941385744754453555A31494F774A6A664C476D416378524E74515549562D5F5F4F46637939694130775F626F6D6F69724A794F6F575A64326E76466E66704F3162314962624B476C747A64357342634E6764486B673D3D',
                      X'6741414141414266364F6C67556E68726750566D51627648314A554A6D536245394D534E392D444A4C4C774647565A4C696B7A432D6A776B625475345F4D4E746452796A70487A436C47666C624C4E6346525447497741696D44706F554B467578506462384C774C396868564552466756504C6165785F317976416E62567078364F61514B694E4B38623642',
                      X'6741414141414266364F6C677331427936686B46355F576137746551565244652D38326333616C714772454F4243764C59526C6F507763327269566B7A394D51444B4F42484C6D41704F57646279544D32774567714A4E78414A644931376C5A66773D3D',
                      'Patient',
                      'F',
                      0
                  );

INSERT INTO Users (
                      ID,
                      username,
                      passCode,
                      birthday,
                      firstName,
                      lastName,
                      phoneNo,
                      HomeAddress,
                      postCode,
                      UserType,
                      Deactivated,
                      LoginCount
                  )
                  VALUES (
                      '3334567878',
                      'testPatient3',
                      '8c42cebd56e6893854c421e0437643a0773ee9bc52d43168670e67132fd1d864',
                      X'6741414141414266364F6C677A7A6834322D53537A534C53424E4C784168526559754563455862705353595844486A33387855566976464150353079396A5F6F466D746B68594E7455654C30506F7A344551623058445155757830395F4E554D2D513D3D',
                      X'6741414141414266364F6C676D45526B3969317364577A6672486E76795F54655A687768672D567978335A4B793459304E7367386E3153624C70775A746F416E44537A654E4F6F6A33343351655752635A5731575579565364507A74754B2D527967416468702D566E62314146547A494531496664636B3D',
                      X'6741414141414266364F6C6744426870476C3564706E374B37464B64744E426151644C363433335A55476E4241734F4D586C315A5A7A36314C7178307565306F6F4A3263684F326E555055427076674B55344F52466A4B4F31324A4C7631505447755961584A326C4453694F63334F4450584E344674773D',
                      X'6741414141414266364F6C6738656962545A4D2D376679565A35464E636535713664454D797539436A54384D7463464B6B714B634A4253325A764F4B2D48696A464B724A4D64724A6764764A346D39567670694553512D436754625165454A4979673D3D',
                      X'6741414141414266364F6C6761664C322D5234692D475741784C43786241497867416D7858484552553931355663365A54784F486834675F766B5A30534239484473464D304532777071535F756551556C544D4A417A42347350735547526F43762D75774F344A50486F2D594C774469674F76684D58653631775434536B6D5564705F436736596C36705053',
                      X'6741414141414266364F6C677A43344470492D7437524A30422D5F674E76394F52614D77572D35736F7333655363475646704A746950393877657A4432344C363964766E77555053436A31306A43696D465641787854597A7A746B314F4F366C6B413D3D',
                      'Patient',
                      'F',
                      0
                  );

INSERT INTO Users (
                      ID,
                      username,
                      passCode,
                      birthday,
                      firstName,
                      lastName,
                      phoneNo,
                      HomeAddress,
                      postCode,
                      UserType,
                      Deactivated,
                      LoginCount
                  )
                  VALUES (
                      'AD1',
                      'testAdmin124',
                      '5ef368722bf09031ced7372c90df64c99a750724ec6dff3e5cf00bb5fcf75c08',
                      X'6741414141414266364F6C67386F4D5F3546394138336A483639546356617A74364A46537872505648746132707036784E6D5542464B6B745F643857573364585A7A4254667949704F52313931386D336449367332784A34324631626D66375435673D3D',
                      X'6741414141414266364F6C675F755F6D544E62303262426F32646C593273796C72726E534E6357576B2D70557442776D5451666A65334D41533345413268592D33742D4C5533386A7268365A7541737A2D63725236336A6E566A63545F39485866577251516A557442375F76594B546E5F6A677A324C493D',
                      X'6741414141414266364F6C67654331636B67534E4C7544544E514F582D5851634E366F5F4F4A38395F64455A526C634F6947305A797464574C394A437074725375536B5A4170657867503558456A397A79576B49416B675A4630675F7452767158505033325866596842367548343369704239796E39553D',
                      X'6741414141414266364F6C674E642D586353423576426C586E5271454D4F49776B38315366486D4C4D394136323673395A6630644142494F554D516F36364358597076587846685A526A43534A345342686666614D575777707379585732645F62673D3D',
                      X'6741414141414266364F6C674F4A644A41376E4A5335644A5A70335F3639696A765A4B786857654A6375585968754B50474C3456754F4554746A554563344E78455541554A70734D384167656143796467695559646E4B5570745A4179346D4C6E4A30306F7362366D7035325842575F644F344167705570307A6F73416646346B2D754743556F532D57714D',
                      X'6741414141414266364F6C677870792D775264694D677645536E39764469586B2D4E3434326C397558744562365A6F4F5932646162333961666638537445474A37325A476C7961353335454D494F53435832634847415F624A4F393536394F642D673D3D',
                      'Admin',
                      'F',
                      0
                  );

INSERT INTO Users (
                      ID,
                      username,
                      passCode,
                      birthday,
                      firstName,
                      lastName,
                      phoneNo,
                      HomeAddress,
                      postCode,
                      UserType,
                      Deactivated,
                      LoginCount
                  )
                  VALUES (
                      'AD2',
                      'testAdmin2',
                      'cec02af7861bcacc36d2b3f9fa3647a0db88e55e1830db44c84be02c0ca1973e',
                      X'6741414141414266364F6C67394D4A4D62634C76585450516730646443496E735F384B4253707058584B44374732624B77396A73326E596F465F5756343276334B6D425F7642466D67614E686257315257346E314F625565305042485964343336513D3D',
                      X'6741414141414266364F6C6730744D727A704B52466870717A6B764D42786B5A494B4B6136376E6B475161685049424B4D7A32436477695A3563544F3952647976434479484B4C6532616B6C615F5F4E363249534B34356E4B4745425F5339737555584D44305A34505F5064672D644D447059366966453D',
                      X'6741414141414266364F6C674E36507257776D4C33354E59595F6E6751643636466E6F4547514F515434484C716E79376464452D6B48727278594F4B444E6D4E744C345F4E784639524C7A56414C71677466594459766B366C7775554651456642666234664D547230615352613262544A7A355A6D57513D',
                      X'6741414141414266364F6C6776716D575256593776667A53636A75545A5573544A34496C756F797550774B6B2D3769725344617833645A697A7A34315668623262333679564C7A4A4C58774E4A372D4B4E304656546A506578744C637357537377673D3D',
                      X'6741414141414266364F6C676E79324A5770547750646E792D5861683868495F4962744D617763467647545833367A41756A6B42674B4E5261636C2D3238665577785062445877352D50335F63475447424A506B7471486C76526C706D566F32387A4E6A4B5477787364776347664F747974795072353556645871345452614B384556696737595A3251714B',
                      X'6741414141414266364F6C67387458707064496D2D4D4F4A6E444472686F526A537769456E6858435045773043364479716F3135655151556A53356C62397A303045706D304D7A426D7544317443386B5A52334E344D34716F50526454344A4343673D3D',
                      'Admin',
                      'F',
                      0
                  );

INSERT INTO Users (
                      ID,
                      username,
                      passCode,
                      birthday,
                      firstName,
                      lastName,
                      phoneNo,
                      HomeAddress,
                      postCode,
                      UserType,
                      Deactivated,
                      LoginCount
                  )
                  VALUES (
                      'AD3',
                      'testAdmin3',
                      '4907d8d8aa1bd2b645438769ecbd744cfd4a1b95cec3b4395a7d5ea2ba7698f3',
                      X'6741414141414266364F6C676B3363666738373345565879746E79515542706857327431696937377873666972697356342D415A6C556E474646347973784E735278377670746A31324563506F6A727034786B666933666F58364E787853377837673D3D',
                      X'6741414141414266364F6C6750566E65765556706565327A684B5F706A334D705A6E536972454F4F5F457A717439392D734E6D7A7263462D3576326E42674E39522D4D383465527170766156776A366632465F4C47724D7A55356D5F45434D705F48675072684C6E6C5242346F697343454B61385142773D',
                      X'6741414141414266364F6C677545654F6975685139743534397A434334766F6F366B39394963326F336B344633622D35473632525A736F41566559785834434A6272465163634F366F68366F654554436B3850594A5332385443457165595341353736427437545A7875424538522D35647346364972493D',
                      X'6741414141414266364F6C6761595A544C354A4B4C334E737339625A72477A4B426B715537697A4654446879726E6F436343337438485F656F6B7A6E4F726C6330754376314E624B4B5A33485052467266686833654A6E69536847576B38616475673D3D',
                      X'6741414141414266364F6C67585639765630713350705A486C536E616A4938783563626A6F61576C4E6E4553306E66476A4F463543645274392D6D68624F4D426F73556361334B426152676E5758796872725173794E745046432D47433673326536496D7A4852433253535F415A696575616D734A684C473876615756356A7964734F6C3459674A39735F57',
                      X'6741414141414266364F6C676C3267716C7733303847495034694E4F6C58706B356648735F613552554A3449646936756C67586E78516B304E6E327A587678764C4952755A6E534D554D4F6C69425F4F73656833696C6B714B5646757373615461413D3D',
                      'Admin',
                      'F',
                      0
                  );

INSERT INTO Users (
                      ID,
                      username,
                      passCode,
                      birthday,
                      firstName,
                      lastName,
                      phoneNo,
                      HomeAddress,
                      postCode,
                      UserType,
                      Deactivated,
                      LoginCount
                  )
                  VALUES (
                      'AD4',
                      'testAdmin4',
                      '0d82b97f8b0257ceed7c5f4ebf15474849efa0082055c639defa5b645c63474d',
                      X'6741414141414266364F6C67512D5F49487A2D713369496E2D594C77736D4C324A6A5F616B5A38487870623673307A78394B4E53645362712D7233496F377153735276696B49706B6252324C776E4263466D665575306E4C654A66594142716F6C773D3D',
                      X'6741414141414266364F6C67396D566167314E6F30763279665A4D79794A524C4D5330703355573961647259696A617A556458466B674A786250494E6932364749414B705F6239344576364D635963487A5A6F7178344543445069566C2D715645506D714B6436354B2D6872344A693764486F566B31303D',
                      X'6741414141414266364F6C676843594E5053565268384F43416C4C365750675830726C4A554A7975776C7766674E58697576564E336F527363375F45524F346A5876734B4B314C4C55656F4434496D555366645948625961545874636231586753633064634438314978366A4B666E6E78486A6A2D2D553D',
                      X'6741414141414266364F6C6757326E677432526C76647576506A335A6E64486B34554D546432635F6A485A5F575A634D453843334A624C5832664442444A477A4F547855476D66654649326455797442552D5258725566674E656C594C76556734513D3D',
                      X'6741414141414266364F6C67744D4A2D4E304E6D6E4B54375A53714471445744424448385353695A546B4B53356F46684E774E66794A314E4454473137412D5871716E58742D743979684834787278595632646559522D7030466A4A5A3579325330776E4B6E464D6755724755586F5035616930657332696D7A62706746743769474F645963655565544165',
                      X'6741414141414266364F6C674D6D5735613576376355504A7953554152455A3751344F6C3352676E676859383965466B513041716C6D6E6D356F4B76674A4674424935357542327A4E686B535A774F5570394A72466A79416C4D464669584D7535673D3D',
                      'Admin',
                      'F',
                      0
                  );

INSERT INTO Users (
                      ID,
                      username,
                      passCode,
                      birthday,
                      firstName,
                      lastName,
                      phoneNo,
                      HomeAddress,
                      postCode,
                      UserType,
                      Deactivated,
                      LoginCount
                  )
                  VALUES (
                      '7129681244',
                      'superPatient',
                      'e78de82c2eab7b72762651835e314d930f1993a1e009727879ae2d05446916bf',
                      X'67414141414142663632344E3744594444393377653463487238616C7836745869664C4E7158554E71425034506C556C48567433614B4A795470434D6E3943696B476B644256413178785F4F5978315A7156576E366F5145333130353836504772773D3D',
                      X'67414141414142663632344F49556A733655482D6C56335A71784D4D56437067795332334F706C4D52414F666768567A3973716C70397377675830586C6F6E5A443751734665366862436661553143753937797A3046644662333765324B7A3471513D3D',
                      X'6741414141414266363234504D6F5A666A4E76513972505F617158657338364B3345676345324E3949376B4A797959314C68773763757936773730414A714D3635455258556D4874556A326F6B50316D3176306B4B4975594778372D4F6E747573673D3D',
                      X'674141414141426636323454725953544F6E62587A6D396567336E794E4B77784B5F2D704451557A3477463563525F446350467865436631474F44377934554D4A4E426E7239585839644C5930336D376547715A4647326D3468646D495F633634673D3D',
                      X'674141414141426636323457552D4759556662716D364250504E596F66442D694C7A4756513539514E6A776838614C4C67357972384D4C766170346249506A73373736783372695A5A766F61614E6F4B4D6E31456535726F6E7932413656646B33413D3D',
                      X'674141414141426636323459713053646C436F354C5276317141517A54646D304E47474174574F4D4A326A38366230443331334173424F33746E745553527856396A6C6B39734A5F4B4C55556C7833705A6C3567357446454D704F5A34422D6774673D3D',
                      'Patient',
                      'F',
                      0
                  );


-- Table: Visit
DROP TABLE IF EXISTS Visit;

CREATE TABLE Visit (
    BookingNo   INTEGER,
    NHSNo       VARCHAR (10) NOT NULL
                             CHECK ("NHSNo" BETWEEN 1000000000 AND 9999999999),
    StaffID     VARCHAR (10) NOT NULL,
    Timeslot    DATETIME     NOT NULL,
    PatientInfo BLOB,
    Confirmed   CHAR (1)     NOT NULL
                             DEFAULT 'P'
                             CHECK (Confirmed IN ('T', 'F', 'P') ),
    Attended    CHAR (1)     CHECK (Attended IN ('T', 'F') ),
    Diagnosis   BLOB,
    Notes       BLOB,
    Rating      INT          CHECK ("Rating" >= 0 OR 
                                    "Rating" <= 5),
    PRIMARY KEY (
        BookingNo
    ),
    FOREIGN KEY (
        NHSNo
    )
    REFERENCES Patient (NHSNo) ON DELETE CASCADE
                               ON UPDATE CASCADE,
    FOREIGN KEY (
        StaffID,
        Timeslot
    )
    REFERENCES available_time (StaffID,
    Timeslot) ON DELETE CASCADE
              ON UPDATE CASCADE,
    FOREIGN KEY (
        StaffID
    )
    REFERENCES GP (ID) ON DELETE CASCADE
                       ON UPDATE CASCADE
);

INSERT INTO Visit (
                      BookingNo,
                      NHSNo,
                      StaffID,
                      Timeslot,
                      PatientInfo,
                      Confirmed,
                      Attended,
                      Diagnosis,
                      Notes,
                      Rating
                  )
                  VALUES (
                      0,
                      '1929282829',
                      'G01',
                      '2020-12-25 11:00:00',
                      '',
                      'T',
                      'F',
                      '',
                      '',
                      5
                  );

INSERT INTO Visit (
                      BookingNo,
                      NHSNo,
                      StaffID,
                      Timeslot,
                      PatientInfo,
                      Confirmed,
                      Attended,
                      Diagnosis,
                      Notes,
                      Rating
                  )
                  VALUES (
                      2,
                      '2929282822',
                      'G02',
                      '2020-12-25 14:00:00',
                      '',
                      'T',
                      'F',
                      '',
                      '',
                      4
                  );

INSERT INTO Visit (
                      BookingNo,
                      NHSNo,
                      StaffID,
                      Timeslot,
                      PatientInfo,
                      Confirmed,
                      Attended,
                      Diagnosis,
                      Notes,
                      Rating
                  )
                  VALUES (
                      3,
                      '3334567878',
                      'G03',
                      '2020-12-25 14:00:00',
                      '',
                      'T',
                      'F',
                      '',
                      '',
                      5
                  );

INSERT INTO Visit (
                      BookingNo,
                      NHSNo,
                      StaffID,
                      Timeslot,
                      PatientInfo,
                      Confirmed,
                      Attended,
                      Diagnosis,
                      Notes,
                      Rating
                  )
                  VALUES (
                      262813,
                      '1929282829',
                      'G02',
                      '2020-12-30 9:15:00',
                      '',
                      'F',
                      'F',
                      '',
                      '',
                      0
                  );

INSERT INTO Visit (
                      BookingNo,
                      NHSNo,
                      StaffID,
                      Timeslot,
                      PatientInfo,
                      Confirmed,
                      Attended,
                      Diagnosis,
                      Notes,
                      Rating
                  )
                  VALUES (
                      584538,
                      '1929282829',
                      'G02',
                      '2020-12-30 9:00:00',
                      '',
                      'F',
                      'F',
                      '',
                      '',
                      0
                  );

INSERT INTO Visit (
                      BookingNo,
                      NHSNo,
                      StaffID,
                      Timeslot,
                      PatientInfo,
                      Confirmed,
                      Attended,
                      Diagnosis,
                      Notes,
                      Rating
                  )
                  VALUES (
                      584539,
                      '1929282829',
                      'G02',
                      '2021-01-01 12:00:00',
                      NULL,
                      'P',
                      NULL,
                      NULL,
                      NULL,
                      NULL
                  );

INSERT INTO Visit (
                      BookingNo,
                      NHSNo,
                      StaffID,
                      Timeslot,
                      PatientInfo,
                      Confirmed,
                      Attended,
                      Diagnosis,
                      Notes,
                      Rating
                  )
                  VALUES (
                      584540,
                      '1929282829',
                      'G01',
                      '2021-01-01 11:00:00',
                      NULL,
                      'T',
                      NULL,
                      X'6741414141414266376A6C4D476B6330774E4F717477556F5254336D4B4444376D64476941414C614E5130785264374F544D626575306369365A6D486B61344B74727956334149536463687333394C316A41766E6B4D526B4E5867444154474932484D696351506D56696F62395166374F7043646655303D',
                      X'6741414141414266376A693561594A6C5864555A726D50746B7A6B2D724257473152625A51513256587738706835677A306748446C46756577354242796D7154347A626C582D7746487958467050573673496E646246484772415F5039576C6930413D3D',
                      NULL
                  );


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
